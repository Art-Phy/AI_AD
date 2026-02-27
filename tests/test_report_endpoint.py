
from fastapi.testclient import TestClient
from aidetect.api.app import app

client = TestClient(app)


def test_report_endpoint_return_report(monkeypatch):
    monkeypatch.setenv("AIDETECT_AUTH_DISABLE", "0")
    monkeypatch.setenv("AIDETECT_API_KEYS", "devkey")
    monkeypatch.setenv("AIDETECT_UI_MODE", "1")

    r = client.post(
        "/v1/analyze/text/report?api_key=devkey",
        json={"text": "Hola mundo. Hola mundo", "mode": "balanced"},
    )
    assert r.status_code == 200
    data = r.json()
    assert "generated_at" in data
    assert "input" in data
    assert "result" in data
    assert data["input"]["mode"] == "balanced"
    assert "score" in data["result"]
    assert "label" in data["result"]



def test_report_is_saved_when_reports_dir_set(monkeypatch, tmp_path):
    monkeypatch.setenv("AIDETECT_AUTH_DISABLED", "0")
    monkeypatch.setenv("AIDETECT_API_KEYS", "devkey")
    monkeypatch.setenv("AIDETECT_UI_MODE", "1")
    monkeypatch.setenv("AIDETECT_REPORTS_DIR", str(tmp_path))

    r = client.post(
        "/v1/analyze/text/report?api_key=devkey",
        json={"text": "Hola mundo", "mode": "balanced"},
    )
    assert r.status_code == 200
    data = r.json()
    assert "saved_to" in data
