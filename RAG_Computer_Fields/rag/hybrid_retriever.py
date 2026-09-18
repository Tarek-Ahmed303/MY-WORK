# ============================================================
# HYBRID RETRIEVER
# ============================================================
# Combines:
#   1. Dense semantic retrieval using BGE + FAISS
#   2. Lexical retrieval using BM25
#   3. Reciprocal Rank Fusion (RRF)
# ============================================================

from rag.retriever import Retriever
from rag.bm25_retriever import BM25Retriever


class HybridRetriever:

    def __init__(
        self,
        dense_top_k=20,
        bm25_top_k=20,
        rrf_k=60
    ):
        """
        Hybrid retrieval using:

        Dense:
            BGE embeddings + FAISS

        Lexical:
            BM25

        Fusion:
            Reciprocal Rank Fusion (RRF)
        """

        self.dense_top_k = dense_top_k
        self.bm25_top_k = bm25_top_k
        self.rrf_k = rrf_k

        print("=" * 70)
        print("INITIALIZING HYBRID RETRIEVER")
        print("=" * 70)

        # ----------------------------------------------------
        # Dense retriever
        # ----------------------------------------------------

        print("\nLoading dense retriever...")

        self.dense_retriever = Retriever()

        print("Dense retriever ready.")

        # ----------------------------------------------------
        # BM25 retriever
        # ----------------------------------------------------

        print("\nLoading BM25 retriever...")

        self.bm25_retriever = BM25Retriever()

        print("BM25 retriever ready.")

        print("\n" + "=" * 70)
        print("HYBRID RETRIEVER READY")
        print("=" * 70)

        print(f"Dense top-k : {self.dense_top_k}")
        print(f"BM25 top-k  : {self.bm25_top_k}")
        print(f"RRF k       : {self.rrf_k}")

    # ========================================================
    # RRF
    # ========================================================

    def _rrf_score(self, rank):
        """
        Reciprocal Rank Fusion score.

        score = 1 / (k + rank)
        """

        return 1.0 / (self.rrf_k + rank)

    # ========================================================
    # RETRIEVE
    # ========================================================

    def retrieve(self, query, top_k=5):

        if query is None:
            raise ValueError("Query cannot be None.")

        query = str(query).strip()

        if not query:
            raise ValueError("Query cannot be empty.")

        # ----------------------------------------------------
        # Dense retrieval
        # ----------------------------------------------------

        dense_results = self.dense_retriever.retrieve(
            query,
            top_k=self.dense_top_k
        )

        # ----------------------------------------------------
        # BM25 retrieval
        # ----------------------------------------------------

        bm25_results = self.bm25_retriever.retrieve(
            query,
            top_k=self.bm25_top_k
        )

        # ----------------------------------------------------
        # Combine results
        # ----------------------------------------------------

        combined = {}

        # ----------------------------------------------------
        # Add dense results
        # ----------------------------------------------------

        for rank, result in enumerate(dense_results, 1):

            doc_id = result["id"]

            if doc_id not in combined:

                combined[doc_id] = {
                    "id": doc_id,
                    "metadata": result["metadata"],
                    "dense_score": result.get("score", 0.0),
                    "bm25_score": 0.0,
                    "dense_rank": rank,
                    "bm25_rank": None,
                    "rrf_score": 0.0
                }

            combined[doc_id]["dense_rank"] = rank

            combined[doc_id]["dense_score"] = result.get(
                "score",
                0.0
            )

            combined[doc_id]["rrf_score"] += self._rrf_score(rank)

        # ----------------------------------------------------
        # Add BM25 results
        # ----------------------------------------------------

        for rank, result in enumerate(bm25_results, 1):

            doc_id = result["id"]

            if doc_id not in combined:

                combined[doc_id] = {
                    "id": doc_id,
                    "metadata": result["metadata"],
                    "dense_score": 0.0,
                    "bm25_score": result.get("score", 0.0),
                    "dense_rank": None,
                    "bm25_rank": rank,
                    "rrf_score": 0.0
                }

            else:

                combined[doc_id]["bm25_rank"] = rank

                combined[doc_id]["bm25_score"] = result.get(
                    "score",
                    0.0
                )

            combined[doc_id]["rrf_score"] += self._rrf_score(rank)

        # ----------------------------------------------------
        # Sort by RRF score
        # ----------------------------------------------------

        ranked_results = sorted(
            combined.values(),
            key=lambda x: x["rrf_score"],
            reverse=True
        )

        # ----------------------------------------------------
        # Return top-k
        # ----------------------------------------------------

        final_results = ranked_results[:top_k]

        # ----------------------------------------------------
        # Standardize score
        # ----------------------------------------------------

        for result in final_results:

            result["score"] = result["rrf_score"]

        return final_results