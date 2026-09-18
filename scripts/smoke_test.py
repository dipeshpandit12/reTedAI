#!/usr/bin/env python3
"""End-to-end smoke test for a running Docker Compose stack."""

import json
import os
from urllib import parse, request

BASE_URL = os.getenv("GATEWAY_BASE_URL", "http://localhost:8080").rstrip("/")


def call(
    path: str,
    method: str = "GET",
    payload: dict[str, str] | None = None,
    headers: dict[str, str] | None = None,
):
    body = json.dumps(payload).encode() if payload is not None else None
    request_headers = dict(headers or {})
    if body:
        request_headers["content-type"] = "application/json"
    req = request.Request(
        f"{BASE_URL}{path}",
        method=method,
        data=body,
        headers=request_headers,
    )
    with request.urlopen(req, timeout=15) as response:
        content_type = response.headers.get("content-type", "")
        body = response.read()
        if response.status >= 400:
            raise RuntimeError(f"{method} {path} returned {response.status}")
        return json.loads(body) if "application/json" in content_type else body.decode()


def main() -> None:
    home = call("/")
    if "reTedAI" not in home or "Cases" not in home:
        raise RuntimeError("Web home page did not render the expected starter UI")

    existing = call("/api/cases")
    if not isinstance(existing, list):
        raise RuntimeError("Case gateway did not return a list")

    issued = call(
        "/api/auth/dev-token",
        "POST",
        {"email": "smoke@retedai.local", "name": "Smoke Tester", "role": "approver"},
    )
    authenticated = call(
        "/api/auth/me",
        headers={"authorization": f"Bearer {issued['access_token']}"},
    )
    if authenticated["role"] != "approver":
        raise RuntimeError("Auth gateway did not resolve the development session")

    created = call(
        "/api/cases",
        "POST",
        {
            "title": "Docker end-to-end smoke test",
            "summary": "A disposable case created by the repository smoke-test script.",
        },
    )
    case_id = created["id"]
    detail = call(f"/api/cases/{case_id}")
    if detail["status"] != "open":
        raise RuntimeError("Created case was not open")

    approved = call(
        f"/api/cases/{case_id}/approve",
        "POST",
        {"note": "Approved by Docker smoke test"},
    )
    if approved["status"] != "approved":
        raise RuntimeError("Gateway approval flow did not complete")

    results = call(f"/api/knowledge/search?q={parse.quote('database latency')}")
    if not isinstance(results, list):
        raise RuntimeError("Knowledge gateway did not return a list")

    print(
        json.dumps(
            {
                "status": "ok",
                "home": "rendered",
                "auth": authenticated["email"],
                "case_id": case_id,
                "approval": approved["status"],
                "knowledge_results": len(results),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
