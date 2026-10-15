
from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

# Replace this import with the module where you move
# your existing, working pipeline initialization.
from rag.service import get_pipeline

app = FastAPI(
    title="Flame in Freefall API",
    description="Evidence-backed microgravity combustion research",
    version="1.0.0",
)

pipeline = None


class AskRequest(BaseModel):
    question: str = Field(min_length=3, max_length=2000)


@app.on_event("startup")
def startup():
    global pipeline
    pipeline = get_pipeline()


@app.get("/health")
def health():
    return {
        "status": "ok",
        "pipeline_loaded": pipeline is not None,
    }


@app.post("/ask")
def ask(request: AskRequest) -> dict[str, Any]:
    if pipeline is None:
        raise HTTPException(
            status_code=503,
            detail="RAG pipeline is not initialized.",
        )

    try:
        result = pipeline.answer(request.question)

        # Your pipeline returns a wrapper containing "response".
        response = result.get("response", result)

        if not isinstance(response, dict):
            raise ValueError("Pipeline response must be a dictionary.")

        return {
            "question": request.question,
            "answer": response.get("answer", ""),
            "experimental_evidence": response.get(
                "experimental_evidence", []
            ),
            "prediction": response.get("prediction"),
            "observed_trends": response.get("observed_trends", []),
            "interpretation": response.get("interpretation", ""),
            "safety_insight": response.get("safety_insight", ""),
            "limitations": response.get("limitations", []),
            "sources": response.get("sources", []),
            "model_used": response.get("model_used"),
            "answerability": result.get("answerability", {}),
            "prediction_notice": (
                "ML predictions use simulated training data and "
                "are not certified fire-safety guidance."
            ),
        }

    except HTTPException:
        raise
    except Exception as exc:
        import traceback
        traceback.print_exc()
        raise HTTPException(
              status_code=500,
              detail=f"{type(exc).__name__}: {exc}",
        ) from exc