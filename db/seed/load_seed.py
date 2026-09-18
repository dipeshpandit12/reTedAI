#!/usr/bin/env python3
import json
import os
from pathlib import Path
from urllib import request

ROOT = Path(__file__).parent
CASE_URL = os.getenv("CASE_SERVICE_URL", "http://localhost:8001")
KNOWLEDGE_URL = os.getenv("KNOWLEDGE_SERVICE_URL", "http://localhost:8003")


def post(url: str, payload: dict[str, str]) -> None:
    body = json.dumps(payload).encode()
    req = request.Request(url, data=body, headers={"content-type": "application/json"})
    with request.urlopen(req, timeout=10) as response:
        if response.status not in {200, 201}:
            raise RuntimeError(f"Seed request failed: {url} ({response.status})")


def main() -> None:
    cases = json.loads((ROOT / "past_cases.json").read_text())
    for item in cases:
        post(f"{CASE_URL}/cases", {"title": item["title"], "summary": item["summary"]})
        post(f"{KNOWLEDGE_URL}/documents", {"title": item["title"], "content": item["resolution"]})

    for runbook in sorted((ROOT / "runbooks").glob("*.md")):
        post(f"{KNOWLEDGE_URL}/documents", {"title": runbook.stem.replace("-", " ").title(), "content": runbook.read_text()})

    print(f"Loaded {len(cases)} cases and runbooks into the local services.")


if __name__ == "__main__":
    main()
