
import importlib

from fastapi.testclient import TestClient



def make_client(monkeypatch):
    # Auth configurada
    monkeypatch.setenv("AIDETECT_AUTH_DISABLED", "0")
    monkeypatch.setenv("AIDETECT_API_KEYS", "devkey")

    # Rate limit muy bajo para test (3 requests por ventana)
    monkeypatch.setenv("AIDETECT_RATE_LIMIT_REQUESTS", "3")
    monkeypatch.setenv("AIDETECT_RATE_LIMIT_WINDOW_SECONDS", "60")

    # Importa (o recarga) el módulo para que el limiter coja los env vars
    import aidetect.api.app as app_module
    importlib.reload(app_module)

    # Reseteamos contadores por si acaso
    app_module.limiter.reset()

    return TestClient(app_module.app)



def test_rate_limit_returns_429(monkeypatch):
    client = make_client(monkeypatch)

    # 3 requests OK
    for _ in range(3):
        r = client.get("/v1/modes", headers={"X-API-Key": "devkey"})
        assert r.status_code == 200

    # 4ª request -> 429
    r = client.get("/v1/modes", headers={"X-API-Key": "devkey"})
    assert r.status_code == 429
    assert r.json()["detail"] == "Rate limit exceeded"



def test_rate_limit_is_per_key(monkeypatch):
    # Permitimos 2 keys
    monkeypatch.setenv("AIDETECT_AUTH_DISABLED", "0")
    monkeypatch.setenv("AIDETECT_API_KEYS", "k1,k2")
    monkeypatch.setenv("AIDETECT_RATE_LIMIT_REQUESTS", "2")
    monkeypatch.setenv("AIDETECT_RATE_LIMIT_WINDOW_SECONDS", "60")

    import aidetect.api.app as app_module
    importlib.reload(app_module)
    app_module.limiter.reset()

    client = TestClient(app_module.app)

    # k1 consume su cuota
    assert client.get("/v1/modes", headers={"X-API-Key": "k1"}).status_code == 200
    assert client.get("/v1/modes", headers={"X-API-Key": "k1"}).status_code == 200
    assert client.get("/v1/modes", headers={"X-API-Key": "k1"}).status_code == 429

    # k2 tiene su propia cuota independiente
    assert client.get("/v1/modes", headers={"X-API-Key": "k2"}).status_code == 200
    assert client.get("/v1/modes", headers={"X-API-Key": "k2"}).status_code == 200
    assert client.get("/v1/modes", headers={"X-API-Key": "k2"}).status_code == 429
