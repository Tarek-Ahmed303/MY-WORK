from sentence_transformers import CrossEncoder


class Reranker:

    def __init__(
        self,
        model_name="cross-encoder/ms-marco-MiniLM-L-6-v2"
    ):

        print("=" * 70)
        print("INITIALIZING CROSS-ENCODER RERANKER")
        print("=" * 70)

        print("\nLoading model:")
        print(model_name)

        self.model = CrossEncoder(model_name)

        print("\nReranker loaded successfully.")

    def rerank(self, query, results, top_k=5):

        if not results:
            return []

        # --------------------------------------------------
        # Build query-document pairs
        # --------------------------------------------------

        pairs = []

        for result in results:

            metadata = result["metadata"]

            # Your metadata is nested:
            if "metadata" in metadata:
                metadata = metadata["metadata"]

            question = metadata["question"]

            pairs.append([
                query,
                question
            ])

        # --------------------------------------------------
        # Cross-encoder scores
        # --------------------------------------------------

        scores = self.model.predict(pairs)

        # --------------------------------------------------
        # Attach reranker score
        # --------------------------------------------------

        reranked = []

        for result, score in zip(results, scores):

            result_copy = result.copy()

            result_copy["reranker_score"] = float(score)

            reranked.append(result_copy)

        # --------------------------------------------------
        # Sort by cross-encoder score
        # --------------------------------------------------

        reranked.sort(
            key=lambda x: x["reranker_score"],
            reverse=True
        )

        return reranked[:top_k]