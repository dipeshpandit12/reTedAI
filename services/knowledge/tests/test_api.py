from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health() -> None:
    assert client.get("/health").json() == {"status": "ok", "service": "knowledge"}


def test_create_and_search_document() -> None:
    created = client.post(
        "/documents",
        json={"title": "Database latency", "content": "Check slow queries and missing indexes during checkout incidents."},
    )
    assert created.status_code == 201
    results = client.get("/search", params={"q": "slow queries"})
    assert results.status_code == 200
    assert any(item["title"] == "Database latency" for item in results.json())
