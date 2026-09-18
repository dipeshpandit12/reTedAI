import math

from .db import repository
from .embeddings import embed
from .models import SearchResult


def cosine(left: list[float], right: list[float]) -> float:
    denominator = math.sqrt(sum(x * x for x in left)) * math.sqrt(sum(x * x for x in right))
    return sum(x * y for x, y in zip(left, right, strict=True)) / denominator if denominator else 0.0


def search(query: str) -> list[SearchResult]:
    query_words = set(query.lower().split())
    query_vector = embed(query)
    results: list[SearchResult] = []
    for document in repository.documents.values():
        words = set(f"{document.title} {document.content}".lower().split())
        keyword_score = len(query_words & words) / max(len(query_words), 1)
        vector_score = (cosine(query_vector, document.chunks[0].vector) + 1) / 2
        score = round((0.7 * keyword_score) + (0.3 * vector_score), 4)
        if score > 0.05:
            results.append(SearchResult(id=document.id, title=document.title, content=document.content, score=score))
    return sorted(results, key=lambda item: item.score, reverse=True)[:10]
