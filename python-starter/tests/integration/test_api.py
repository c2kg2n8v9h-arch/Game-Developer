from fastapi.testclient import TestClient
from rag_service.api.app import app


def test_health_endpoint() -> None:
    response = TestClient(app).get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_and_get_local_world() -> None:
    client = TestClient(app)
    created = client.post("/v1/worlds", json={"description": "A floating forest"})
    assert created.status_code == 202
    payload = created.json()
    assert payload["provider"] == "local"

    fetched = client.get(f"/v1/worlds/{payload['id']}")
    assert fetched.status_code == 200
    assert fetched.json()["assets"][0]["kind"] == "manifest"
