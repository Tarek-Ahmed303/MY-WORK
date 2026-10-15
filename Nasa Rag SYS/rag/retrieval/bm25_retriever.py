import json
from pathlib import Path

from rank_bm25 import BM25Okapi


PROJECT_ROOT = Path(
    r"C:\Users\User\Nasa Rag SYS\rag"
)

CHUNKS_FILE = (
    PROJECT_ROOT
    / "embeddings"
    / "processed"
    / "chunks"
    / "chunks.json"
)


class BM25Retriever:

    def __init__(
        self,
        chunks_file=CHUNKS_FILE
    ):

        self.chunks_file = Path(
            chunks_file
        )

        if not self.chunks_file.exists():
            raise FileNotFoundError(
                f"Chunks file not found: {self.chunks_file}"
            )

        with open(
            self.chunks_file,
            "r",
            encoding="utf-8"
        ) as f:

            self.chunks = json.load(f)

        self.tokenized_corpus = [
            self.tokenize(
                chunk.get("text", "")
            )
            for chunk in self.chunks
        ]

        self.bm25 = BM25Okapi(
            self.tokenized_corpus
        )

    @staticmethod
    def tokenize(text):

        return text.lower().split()

    def search(self, query, top_k=10):

        query_tokens = self.tokenize(
            query
        )

        scores = self.bm25.get_scores(
            query_tokens
        )

        ranked_indices = sorted(
            range(len(scores)),
            key=lambda i: scores[i],
            reverse=True
        )

        results = []

        for rank, index in enumerate(
            ranked_indices[:top_k],
            start=1
        ):

            results.append({
                "chunk_id": int(index),
                "score": float(scores[index]),
                "rank": rank
            })

        return results