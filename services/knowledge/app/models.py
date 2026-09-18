from uuid import uuid4

from pydantic import BaseModel, Field


class Chunk(BaseModel):
    content: str
    vector: list[float] = Field(default_factory=list)


class Document(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    title: str
    content: str
    chunks: list[Chunk] = Field(default_factory=list)


class SearchResult(BaseModel):
    id: str
    title: str
    content: str
    score: float
