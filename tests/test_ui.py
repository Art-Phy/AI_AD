
from fastapi.testclient import TestClient
from aidetect.api.app import app

client = TestClient(app)

def test_ui_page_loads():
    r = client.get("/ui")
    assert r.status_code == 200
    assert "AI Authorship Detector" in r.text
