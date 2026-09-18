import os

import httpx


async def call_llm(prompt: str) -> str:
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")

    async with httpx.AsyncClient(timeout=30) as client:
        if anthropic_key:
            response = await client.post(
                "https://api.anthropic.com/v1/messages",
                headers={
                    "x-api-key": anthropic_key,
                    "anthropic-version": "2023-06-01",
                },
                json={
                    "model": os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-5"),
                    "max_tokens": 700,
                    "messages": [{"role": "user", "content": prompt}],
                },
            )
            response.raise_for_status()
            return response.json()["content"][0]["text"]

        if openai_key:
            response = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers={"authorization": f"Bearer {openai_key}"},
                json={
                    "model": os.getenv("OPENAI_MODEL", "gpt-5-mini"),
                    "messages": [{"role": "user", "content": prompt}],
                },
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]

    return "Local fallback: review the matched runbooks, verify recent changes, and collect service metrics before approving remediation."
