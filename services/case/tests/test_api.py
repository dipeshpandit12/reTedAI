from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "case"}


def test_create_get_and_approve_case() -> None:
    created = client.post(
        "/cases",
        json={"title": "Database latency", "summary": "Checkout queries exceed two seconds."},
    )
    assert created.status_code == 201
    case_id = created.json()["id"]

    assert client.get(f"/cases/{case_id}").status_code == 200

    forbidden = client.post(f"/cases/{case_id}/approve", json={"note": "looks good"})
    assert forbidden.status_code == 403

    approved = client.post(
        f"/cases/{case_id}/approve",
        json={"note": "Validated"},
        headers={"x-user-id": "reviewer", "x-user-role": "approver"},
    )
    assert approved.status_code == 200
    assert approved.json()["status"] == "approved"
