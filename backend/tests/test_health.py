from fastapi.testclient import TestClient

from app.main import app, ollama


def test_api_health() -> None:
    response = TestClient(app).get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "trustlens-api"}


def test_serpapi_health_does_not_make_a_search() -> None:
    response = TestClient(app).get("/api/health/serpapi")
    assert response.status_code == 200
    assert response.json()["available"] is None


def test_ollama_health_with_mocked_local_service(monkeypatch) -> None:
    async def fake_health():
        return True, True

    monkeypatch.setattr(ollama, "health", fake_health)
    response = TestClient(app).get("/api/health/ollama")
    assert response.status_code == 200
    assert response.json()["available"] is True
