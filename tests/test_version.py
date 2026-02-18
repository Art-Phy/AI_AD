
from fastapi.testclient import TestClient
from aidetect.api.app import app

client = TestClient(app)

def test_version_endpoint():
    r = client.get("/version")
    assert r.status_code == 200
    assert "version" in r.json()
    assert isinstance(r.json()["version"], str)
