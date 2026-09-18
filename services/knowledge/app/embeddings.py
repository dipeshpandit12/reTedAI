import hashlib


def embed(text: str, dimensions: int = 16) -> list[float]:
    """Deterministic local embedding seam; replace with the chosen provider."""
    digest = hashlib.sha256(text.encode("utf-8")).digest()
    return [round((digest[index] / 127.5) - 1, 6) for index in range(dimensions)]
