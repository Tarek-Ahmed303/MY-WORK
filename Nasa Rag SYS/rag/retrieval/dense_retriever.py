from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


PROJECT_ROOT = Path(
    r"C:\Users\User\Nasa Rag SYS\rag"
)

INDEX_FILE = (
    PROJECT_ROOT
    / "vector_store"
    / "processed"
    / "vector_store"
    / "faiss.index"
)

MODEL_NAME = "BAAI/bge-small-en-v1.5"


class DenseRetriever:

    def __init__(
        self,
        index_file=INDEX_FILE,
        model_name=MODEL_NAME
    ):

        self.index_file = Path(index_file)

        if not self.index_file.exists():
            raise FileNotFoundError(
                f"FAISS index not found: {self.index_file}"
            )

        self.index = faiss.read_index(
            str(self.index_file)
        )

        self.model = SentenceTransformer(
            model_name
        )

    def encode_query(self, query):

        embedding = self.model.encode(
            query,
            normalize_embeddings=True
        )

        embedding = np.asarray(
            embedding,
            dtype=np.float32
        )

        return embedding.reshape(1, -1)

    def search(self, query, top_k=10):

        query_embedding = self.encode_query(
            query
        )

        scores, indices = self.index.search(
            query_embedding,
            top_k
        )

        results = []

        for rank, (score, index) in enumerate(
            zip(scores[0], indices[0]),
            start=1
        ):

            if index == -1:
                continue

            results.append({
                "chunk_id": int(index),
                "score": float(score),
                "rank": rank
            })

        return results