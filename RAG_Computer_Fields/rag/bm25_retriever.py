import pickle
from pathlib import Path

from rank_bm25 import BM25Okapi


class BM25Retriever:

    def __init__(self):

        # ============================================================
        # PROJECT ROOT
        # ============================================================

        PROJECT_ROOT = Path(__file__).resolve().parent.parent

        # ============================================================
        # DATA FILE
        # ============================================================

        DATA_FILE = (
            PROJECT_ROOT
            / "data"
            / "embeddings"
            / "question_embeddings.pkl"
        )

        # ============================================================
        # LOAD QUESTIONS
        # ============================================================

        print("=" * 70)
        print("INITIALIZING BM25")
        print("=" * 70)

        print("\nLoading question data...")

        with open(DATA_FILE, "rb") as f:
            data = pickle.load(f)

        print("Records loaded:", len(data))

        # ============================================================
        # EXTRACT QUESTIONS
        # ============================================================

        self.questions = []
        self.metadata = []

        for item in data:

            metadata = item["metadata"]

            # Your metadata is nested
            if "metadata" in metadata:
                metadata = metadata["metadata"]

            question = metadata.get("question")

            if not question:
                continue

            self.questions.append(question)
            self.metadata.append(metadata)

        print("Questions extracted:", len(self.questions))

        # ============================================================
        # TOKENIZE QUESTIONS
        # ============================================================

        tokenized_questions = [
            self.tokenize(question)
            for question in self.questions
        ]

        # ============================================================
        # BUILD BM25 INDEX
        # ============================================================

        print("\nBuilding BM25 index...")

        self.bm25 = BM25Okapi(
            tokenized_questions
        )

        print("BM25 index built successfully.")

        print("\n" + "=" * 70)
        print("BM25 READY")
        print("=" * 70)

    # ================================================================
    # TOKENIZER
    # ================================================================

    @staticmethod
    def tokenize(text):

        return text.lower().split()

    # ================================================================
    # RETRIEVE
    # ================================================================

    def retrieve(self, query, top_k=5):

        if not query:
            raise ValueError(
                "Query cannot be empty."
            )

        query_tokens = self.tokenize(query)

        # Get BM25 scores
        scores = self.bm25.get_scores(
            query_tokens
        )

        # Rank by score
        ranked_indices = sorted(
            range(len(scores)),
            key=lambda i: scores[i],
            reverse=True
        )

        ranked_indices = ranked_indices[:top_k]

        # Build results
        results = []

        for index in ranked_indices:

            results.append({
                "id": self.metadata[index]["id"],
                "score": float(scores[index]),
                "metadata": self.metadata[index]
            })

        return results