from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health() -> None:
    assert client.get("/health").json() == {"status": "ok", "service": "auth"}
    assert client.get("/auth/health").json() == {"status": "ok", "service": "auth"}


def test_development_tokens_are_disabled_by_default(monkeypatch) -> None:
    monkeypatch.delenv("AUTH_MODE", raising=False)
    response = client.post("/auth/dev-token", json={})
    assert response.status_code == 404


def test_development_session_lifecycle(monkeypatch) -> None:
    monkeypatch.setenv("AUTH_MODE", "development")
    issued = client.post(
        "/auth/dev-token",
        json={"email": "reviewer@retedai.local", "name": "Demo Reviewer", "role": "approver"},
    )
    assert issued.status_code == 200
    token = issued.json()["access_token"]
    headers = {"authorization": f"Bearer {token}"}

    current = client.get("/auth/me", headers=headers)
    assert current.status_code == 200
    assert current.json()["role"] == "approver"

    assert client.delete("/auth/session", headers=headers).status_code == 204
    assert client.get("/auth/me", headers=headers).status_code == 401
