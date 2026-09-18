from fastapi import FastAPI, Query, status
from pydantic import BaseModel, Field

from .db import repository
from .models import Document, SearchResult
from .search import search

app = FastAPI(title="reTedAI Knowledge Service", version="0.1.0")


class CreateDocumentRequest(BaseModel):
    title: str = Field(min_length=3, max_length=200)
    content: str = Field(min_length=10)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "knowledge"}


@app.post("/documents", response_model=Document, status_code=status.HTTP_201_CREATED)
def create_document(payload: CreateDocumentRequest) -> Document:
    return repository.add(payload.title, payload.content)


@app.get("/search", response_model=list[SearchResult])
def search_documents(q: str = Query(min_length=1, max_length=500)) -> list[SearchResult]:
    return search(q)
