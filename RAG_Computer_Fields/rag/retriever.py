import pickle
from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


class Retriever:

    def __init__(self, top_k=20):

        # ============================================================
        # PROJECT ROOT
        # ============================================================

        self.project_root = Path(__file__).resolve().parent.parent

        # ============================================================
        # FILE PATHS
        # ============================================================

        self.embeddings_file = (
            self.project_root
            / "data"
            / "embeddings"
            / "question_embeddings.pkl"
        )

        self.index_file = (
            self.project_root
            / "vector_store"
            / "question_index.faiss"
        )

        self.metadata_file = (
            self.project_root
            / "vector_store"
            / "metadata.pkl"
        )

        # ============================================================
        # SETTINGS
        # ============================================================

        self.top_k = top_k

        # ============================================================
        # LOAD EMBEDDING MODEL
        # ============================================================

        print("Loading embedding model...")

        self.model = SentenceTransformer(
            "BAAI/bge-small-en-v1.5"
        )

        print("Embedding model loaded.")
        print(
            "Embedding dimension:",
            self.model.get_embedding_dimension()
        )

        # ============================================================
        # LOAD FAISS INDEX
        # ============================================================

        print("Loading FAISS index...")

        self.index = faiss.read_index(
            str(self.index_file)
        )

        # ============================================================
        # LOAD METADATA
        # ============================================================

        print("Loading metadata...")

        with open(self.metadata_file, "rb") as f:
            self.metadata = pickle.load(f)

        # ============================================================
        # LOAD EMBEDDED QUESTIONS
        # ============================================================

        with open(self.embeddings_file, "rb") as f:
            self.embedded_questions = pickle.load(f)

        # ============================================================
        # VALIDATION
        # ============================================================

        if self.index.ntotal != len(self.metadata):
            raise ValueError(
                "FAISS index and metadata have different sizes."
            )

        print()
        print("=" * 70)
        print("RETRIEVER INITIALIZED")
        print("=" * 70)
        print("Vectors:", self.index.ntotal)
        print("Metadata:", len(self.metadata))
        print("Dimension:", self.index.d)
        print("Top-K:", self.top_k)
        print("=" * 70)

    # ================================================================
    # RETRIEVE
    # ================================================================

    def retrieve(self, query, top_k=None):

        if query is None:
            raise ValueError("Query cannot be None.")

        query = str(query).strip()

        if not query:
            raise ValueError("Query cannot be empty.")

        # ------------------------------------------------------------
        # TOP K
        # ------------------------------------------------------------

        if top_k is None:
            top_k = self.top_k

        # Don't request more vectors than exist
        top_k = min(top_k, self.index.ntotal)

        # ------------------------------------------------------------
        # EMBED QUERY
        # ------------------------------------------------------------

        query_embedding = self.model.encode(
            query,
            normalize_embeddings=True,
            convert_to_numpy=True
        )

        # ------------------------------------------------------------
        # FLOAT32
        # ------------------------------------------------------------

        query_embedding = np.asarray(
            query_embedding,
            dtype=np.float32
        )

        # ------------------------------------------------------------
        # SHAPE
        # ------------------------------------------------------------

        query_embedding = query_embedding.reshape(
            1,
            -1
        )

        # ------------------------------------------------------------
        # FAISS SEARCH
        # ------------------------------------------------------------

        scores, indices = self.index.search(
            query_embedding,
            top_k
        )

        # ------------------------------------------------------------
        # BUILD RESULTS
        # ------------------------------------------------------------

        results = []

        for score, index_id in zip(
            scores[0],
            indices[0]
        ):

            if index_id < 0:
                continue

            metadata = self.metadata[index_id]

            results.append({
                "id": metadata["id"],
                "score": float(score),
                "metadata": metadata
            })

        return results