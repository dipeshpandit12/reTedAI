from .embeddings import embed
from .models import Chunk, Document


class KnowledgeRepository:
    """In-memory development store; PostgreSQL/pgvector is the persistence seam."""

    def __init__(self) -> None:
        self.documents: dict[str, Document] = {}

    def add(self, title: str, content: str) -> Document:
        document = Document(
            title=title,
            content=content,
            chunks=[Chunk(content=content, vector=embed(content))],
        )
        self.documents[document.id] = document
        return document


repository = KnowledgeRepository()
