from fastapi import FastAPI
from pydantic import BaseModel, Field

from .rag import diagnose

app = FastAPI(title="reTedAI AI Service", version="0.2.0")


class DiagnoseRequest(BaseModel):
    case_id: str
    question: str = Field(min_length=5, max_length=5000)


class DiagnoseResponse(BaseModel):
    case_id: str
    diagnosis: str
    sources: list[str]


@app.get("/")
def root() -> dict[str, str]:
    return {"service": "ai"}


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "ai"}


@app.post("/diagnose", response_model=DiagnoseResponse)
async def create_diagnosis(payload: DiagnoseRequest) -> DiagnoseResponse:
    diagnosis, sources = await diagnose(payload.question)
    return DiagnoseResponse(
        case_id=payload.case_id,
        diagnosis=diagnosis,
        sources=sources,
    )
