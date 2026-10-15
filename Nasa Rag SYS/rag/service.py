
"""
Flame in Freefall - RAG Service
Initializes and caches the application's RAG pipeline.
"""

from functools import lru_cache
from threading import Lock
from pathlib import Path

from .pipeline import RAGPipeline

from .retrieval.hybrid_retriever import HybridRetriever
from .retrieval.reranker import CrossEncoderReranker
from .vector_store.Metadata_filter import MetadataFilter
from .context.context_selector import ContextSelector
from .context.context_builder import ContextBuilder
from .answer.answerability import AnswerabilityGate
from .llm.response_generator import ResponseGenerator


_pipeline_lock = Lock()

# Match the chunks file used by the existing retrievers.
RAG_DIR = Path(__file__).resolve().parent
CHUNKS_FILE = (
    RAG_DIR
    / "embeddings"
    / "processed"
    / "chunks"
    / "chunks.json"
)


def create_pipeline_components() -> dict:
    """Initialize the existing RAG components."""

    if not CHUNKS_FILE.exists():
        raise FileNotFoundError(
            f"Chunks file not found: {CHUNKS_FILE}"
        )

    print("=" * 60)
    print("INITIALIZING FLAME IN FREEFALL RAG")
    print("=" * 60)

    components = {
        "retriever": HybridRetriever(),
        "reranker": CrossEncoderReranker(),
        "metadata_filter": MetadataFilter(
            chunks_file=CHUNKS_FILE
        ),
        "context_selector": ContextSelector(top_k=3),
        "context_builder": ContextBuilder(),
        "answerability_gate": AnswerabilityGate(),
        "response_generator": ResponseGenerator(),
    }

    print("All seven RAG components initialized.")
    print("=" * 60)

    return components


@lru_cache(maxsize=1)
def get_pipeline() -> RAGPipeline:
    """Return one initialized RAG pipeline per process."""

    with _pipeline_lock:
        components = create_pipeline_components()

        required_components = [
            "retriever",
            "reranker",
            "metadata_filter",
            "context_selector",
            "context_builder",
            "answerability_gate",
            "response_generator",
        ]

        missing = [
            name
            for name in required_components
            if components.get(name) is None
        ]

        if missing:
            raise RuntimeError(
                "Missing RAG components: " + ", ".join(missing)
            )

        pipeline = RAGPipeline(**components)

        if not callable(getattr(pipeline, "answer", None)):
            raise RuntimeError(
                "RAGPipeline has no callable answer() method."
            )

        print("RAG pipeline initialized successfully.")
        return pipeline
