
from fastapi.testclient import TestClient

from aidetect.api.app import app

client = TestClient(app)



def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"



def test_analyze_text_endpoint():
    r = client.post("/v1/analyze/text", json={"text": "Hola mundo. Hola mundo", "mode": "balanced"})
    assert r.status_code == 200
    data = r.json()
    assert "score" in data
    assert "label" in data
    assert "details" in data
    assert data["details"]["mode"] == "balanced"
