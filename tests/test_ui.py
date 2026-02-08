
from fastapi.testclient import TestClient
from aidetect.api.app import app

client = TestClient(app)

def test_ui_page_loads():
    r = client.get("/ui")
    assert r.status_code == 200
    assert "AI Authorship Detector" in r.text


def test_ui_static_js_served():
    r = client.get("/static/app.js")
    assert r.status_code == 200
    assert "fetch(" in r.text
