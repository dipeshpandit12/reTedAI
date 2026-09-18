from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health() -> None:
    assert client.get("/health").json() == {"status": "ok", "service": "automation"}


def test_whitelisted_action_is_dry_run_by_default(monkeypatch) -> None:
    monkeypatch.delenv("ENABLE_AUTOMATION_EXECUTION", raising=False)
    response = client.post("/executions", json={"action": "disk_usage", "target_container": "case"})
    assert response.status_code == 200
    assert response.json()["status"] == "dry-run"


def test_unknown_action_is_rejected() -> None:
    response = client.post("/executions", json={"action": "shell", "target_container": "case"})
    assert response.status_code == 200
    assert response.json()["status"] == "rejected"
