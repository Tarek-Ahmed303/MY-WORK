from sentence_transformers import CrossEncoder


MODEL_NAME = "cross-encoder/ms-marco-MiniLM-L-6-v2"


class CrossEncoderReranker:

    def __init__(self, model_name=MODEL_NAME):

        print("=" * 60)
        print("CROSS-ENCODER RERANKER")
        print("=" * 60)

        self.model_name = model_name

        print(
            f"Loading model: {model_name}"
        )

        self.model = CrossEncoder(
            model_name
        )

        print(
            "Model loaded successfully."
        )

        print("=" * 60)

    # ========================================================
    # RERANK
    # ========================================================

    def rerank(
        self,
        query,
        candidates,
        top_k=2
    ):

        if not candidates:

            return []

        print("\n" + "=" * 60)
        print("CROSS-ENCODER RERANKING")
        print("=" * 60)

        print(
            f"Query: {query}"
        )

        print(
            f"Candidates received: "
            f"{len(candidates)}"
        )

        # ----------------------------------------------------
        # BUILD QUERY-DOCUMENT PAIRS
        # ----------------------------------------------------

        pairs = []

        for candidate in candidates:

            text = candidate.get(
                "text",
                ""
            )

            pairs.append([
                query,
                text
            ])

        # ----------------------------------------------------
        # PREDICT
        # ----------------------------------------------------

        print(
            "Generating reranker scores..."
        )

        scores = self.model.predict(
            pairs
        )

        # ----------------------------------------------------
        # ATTACH SCORES
        # ----------------------------------------------------

        reranked = []

        for candidate, score in zip(
            candidates,
            scores
        ):

            result = candidate.copy()

            result["reranker_score"] = float(
                score
            )

            reranked.append(
                result
            )

        # ----------------------------------------------------
        # SORT
        # ----------------------------------------------------

        reranked.sort(
            key=lambda x: x[
                "reranker_score"
            ],
            reverse=True
        )

        # ----------------------------------------------------
        # ASSIGN RANK
        # ----------------------------------------------------

        for rank, result in enumerate(
            reranked,
            start=1
        ):

            result[
                "reranker_rank"
            ] = rank

        # ----------------------------------------------------
        # TOP K
        # ----------------------------------------------------

        final_results = reranked[:top_k]

        # ----------------------------------------------------
        # DEBUG OUTPUT
        # ----------------------------------------------------

        print("\n" + "=" * 60)
        print("RERANKING COMPLETE")
        print("=" * 60)

        print(
            f"Top K: {len(final_results)}"
        )

        for result in final_results:

            print("\n" + "-" * 50)

            print(
                f"Reranker Rank: "
                f"{result.get('reranker_rank', 'N/A')}"
            )

            print(
                f"Chunk ID: "
                f"{result.get('chunk_id', 'N/A')}"
            )

            print(
                f"Reranker Score: "
                f"{result.get('reranker_score', 0):.4f}"
            )

            print(
                f"Hybrid Rank: "
                f"{result.get('hybrid_rank', 'N/A')}"
            )

            print(
                f"Dense Rank: "
                f"{result.get('dense_rank', 'N/A')}"
            )

            print(
                f"BM25 Rank: "
                f"{result.get('bm25_rank', 'N/A')}"
            )

        return final_results