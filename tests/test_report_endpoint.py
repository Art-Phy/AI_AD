
import importlib

from fastapi.testclient import TestClient


def make_client(monkeypatch):
    monkeypatch.setenv("AIDETECT_AUTH_DISABLED", "0")
    monkeypatch.setenv("AIDETECT_API_KEYS", "devkey")
    monkeypatch.setenv("AIDETECT_UI_MODE", "1")

    import aidetect.api.app as app_module
    importlib.reload(app_module)

    app_module.limiter.reset()

    return TestClient(app_module.app)


def test_report_endpoint_returns_report(monkeypatch):
    client = make_client(monkeypatch)

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
    monkeypatch.setenv("AIDETECT_REPORTS_DIR", str(tmp_path))
    client = make_client(monkeypatch)

    r = client.post(
        "/v1/analyze/text/report?api_key=devkey",
        json={"text": "Hola mundo", "mode": "balanced"},
    )
    assert r.status_code == 200
    data = r.json()
    assert "saved_to" in data


def test_report_does_not_include_text_by_default(monkeypatch):
    client = make_client(monkeypatch)

    r = client.post(
        "/v1/analyze/text/report?api_key=devkey",
        json={"text": "Hola mundo", "mode": "balanced"},
    )
    assert r.status_code == 200
    data = r.json()
    assert "text" not in data["input"]


def test_report_includes_text_when_requested(monkeypatch):
    client = make_client(monkeypatch)

    r = client.post(
        "/v1/analyze/text/report?api_key=devkey&include_text=true",
        json={"text": "Hola mundo", "mode": "balanced"},
    )
    assert r.status_code == 200
    data = r.json()
    assert data["input"]["text"] == "Hola mundo"
