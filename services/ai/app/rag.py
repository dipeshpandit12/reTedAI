import os

import httpx

from .llm import call_llm
from .prompts import build_prompt


async def diagnose(question: str) -> tuple[str, list[str]]:
    knowledge_url = os.getenv("KNOWLEDGE_SERVICE_URL", "http://localhost:8003")
    context: list[str] = []
    sources: list[str] = []
    try:
        async with httpx.AsyncClient(timeout=3) as client:
            response = await client.get(f"{knowledge_url}/search", params={"q": question})
            response.raise_for_status()
            for result in response.json()[:5]:
                context.append(result["content"])
                sources.append(result["id"])
    except httpx.HTTPError:
        pass

    return await call_llm(build_prompt(question, context)), sources
