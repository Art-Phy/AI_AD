
from fastapi.testclient import TestClient
from aidetect.api.app import app

client = TestClient(app)


def test_request_id_header_present():
    r = client.get("/health")
    assert r.status_code == 200
    assert "X-Request-ID" in r.headers


def test_request_id_preserved_if_sent():
    r = client.get("/health", headers={"X-Request-ID": "my-id-123"})
    assert r.status_code == 200
    assert r.headers["X-Request-ID"] == "my-id-123"

