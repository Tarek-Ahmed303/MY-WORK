from .dense_retriever import DenseRetriever
from .bm25_retriever import BM25Retriever


RRF_K = 60


class HybridRetriever:

    def __init__(
        self,
        dense_retriever=None,
        bm25_retriever=None,
        rrf_k=RRF_K
    ):

        self.dense_retriever = (
            dense_retriever
            if dense_retriever is not None
            else DenseRetriever()
        )

        self.bm25_retriever = (
            bm25_retriever
            if bm25_retriever is not None
            else BM25Retriever()
        )

        self.rrf_k = rrf_k

    def reciprocal_rank_fusion(
        self,
        dense_results,
        bm25_results
    ):

        fused_scores = {}

        # Dense results
        for result in dense_results:

            chunk_id = result["chunk_id"]
            rank = result["rank"]

            if chunk_id not in fused_scores:

                fused_scores[chunk_id] = {
                    "chunk_id": chunk_id,
                    "rrf_score": 0.0,
                    "dense_rank": None,
                    "bm25_rank": None,
                    "dense_score": None,
                    "bm25_score": None
                }

            fused_scores[chunk_id][
                "rrf_score"
            ] += 1.0 / (
                self.rrf_k + rank
            )

            fused_scores[chunk_id][
                "dense_rank"
            ] = rank

            fused_scores[chunk_id][
                "dense_score"
            ] = result["score"]

        # BM25 results
        for result in bm25_results:

            chunk_id = result["chunk_id"]
            rank = result["rank"]

            if chunk_id not in fused_scores:

                fused_scores[chunk_id] = {
                    "chunk_id": chunk_id,
                    "rrf_score": 0.0,
                    "dense_rank": None,
                    "bm25_rank": None,
                    "dense_score": None,
                    "bm25_score": None
                }

            fused_scores[chunk_id][
                "rrf_score"
            ] += 1.0 / (
                self.rrf_k + rank
            )

            fused_scores[chunk_id][
                "bm25_rank"
            ] = rank

            fused_scores[chunk_id][
                "bm25_score"
            ] = result["score"]

        ranked_results = sorted(
            fused_scores.values(),
            key=lambda x: x["rrf_score"],
            reverse=True
        )

        for rank, result in enumerate(
            ranked_results,
            start=1
        ):

            result["hybrid_rank"] = rank

        return ranked_results

    def search(
        self,
        query,
        dense_top_k=10,
        bm25_top_k=10,
        top_k=10
    ):

        dense_results = (
            self.dense_retriever.search(
                query,
                top_k=dense_top_k
            )
        )

        bm25_results = (
            self.bm25_retriever.search(
                query,
                top_k=bm25_top_k
            )
        )

        hybrid_results = (
            self.reciprocal_rank_fusion(
                dense_results,
                bm25_results
            )
        )

        return hybrid_results[:top_k]