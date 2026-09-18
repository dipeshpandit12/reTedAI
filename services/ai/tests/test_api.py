from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "ai"}


def test_diagnose_uses_local_fallback_without_provider_keys(monkeypatch) -> None:
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    response = client.post(
        "/diagnose",
        json={"case_id": "case-1", "question": "Why is checkout latency high?"},
    )
    assert response.status_code == 200
    assert response.json()["case_id"] == "case-1"
    assert "Local fallback" in response.json()["diagnosis"]
