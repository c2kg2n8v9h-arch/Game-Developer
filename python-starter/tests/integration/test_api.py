from fastapi.testclient import TestClient
from rag_service.api.app import app


def test_health_endpoint() -> None:
    response = TestClient(app).get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_game_page() -> None:
    response = TestClient(app).get("/game")
    assert response.status_code == 200
    assert "Lorebound" in response.text
    assert "/v1/datasets/hugging-face" in response.text
    assert "/v1/ai/npc/turn" in response.text


def test_ai_capabilities() -> None:
    response = TestClient(app).get("/v1/ai/capabilities")
    assert response.status_code == 200
    assert response.json()["npc_provider"] == "local"
    assert response.json()["huggingface_token_configured"] is False


def test_structured_local_npc_turn() -> None:
    client = TestClient(app)
    client.post("/v1/documents", json={"document_id": "lore:test", "content": "The silver path leads to the moon gate."})
    response = client.post(
        "/v1/ai/npc/turn",
        json={"character": "The Cartographer", "player_message": "Where does the silver path lead?"},
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["emotion"] == "curious"
    assert "silver path" in payload["speech"].lower()
    assert payload["actions"] == []


def test_create_and_get_local_world() -> None:
    client = TestClient(app)
    created = client.post("/v1/worlds", json={"description": "A floating forest"})
    assert created.status_code == 202
    payload = created.json()
    assert payload["provider"] == "local"

    fetched = client.get(f"/v1/worlds/{payload['id']}")
    assert fetched.status_code == 200
    assert fetched.json()["assets"][0]["kind"] == "manifest"
