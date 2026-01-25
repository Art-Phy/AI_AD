
from fastapi.testclient import TestClient

from aidetect.api.app import app

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_analyze_text_requires_api_key(monkeypatch):
    # Aseguramos que auth NO está desactivada y que existe una key válida
    monkeypatch.setenv("AIDETECT_AUTH_DISABLED", "0")
    monkeypatch.setenv("AIDETECT_API_KEYS", "devkey")

    # Sin API key -> 401
    r = client.post("/v1/analyze/text", json={"text": "Hola mundo. Hola mundo", "mode": "balanced"})
    assert r.status_code == 401


def test_analyze_text_with_valid_api_key(monkeypatch):
    monkeypatch.setenv("AIDETECT_AUTH_DISABLED", "0")
    monkeypatch.setenv("AIDETECT_API_KEYS", "devkey")

    # Con API key válida -> 200
    r = client.post(
        "/v1/analyze/text",
        headers={"X-API-Key": "devkey"},
        json={"text": "Hola mundo. Hola mundo", "mode": "balanced"},
    )
    assert r.status_code == 200
    data = r.json()
    assert "score" in data
    assert "label" in data
    assert "details" in data
    assert data["details"]["mode"] == "balanced"
