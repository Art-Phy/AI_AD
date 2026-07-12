
"""
Configuración central del detector.

Más adelante podrá cargarse desde archivo o variables de entorno.
"""

DEFAULT_MODE = "balanced"

MODES = {
    "conservative": {
        "ai_threshold": 0.85,
        "human_threshold": 0.30,
        "description": "Minimiza falsos positivos. Solo clasifica como IA con alta confianza.",
    },
    "balanced": {
        "ai_threshold": 0.70,
        "human_threshold": 0.40,
        "description": "Equilibrio entre precisión y cobertura.",
    },
    "aggressive": {
        "ai_threshold": 0.55,
        "human_threshold": 0.45,
        "description": "Maximiza detección de IA, asumiendo más riesgo de falsos positivos.",
    },
}


import os


def get_api_keys() -> set[str]:
    """
    Devuelve el set de API keys válidas desde la variable de entorno.

    Formato:
        AIDETECT_API_KEYS="key1,key2,key3"
    """
    raw = os.getenv("AIDETECT_API_KEYS", "").strip()
    if not raw:
        return set()
    return {k.strip() for k in raw.split(",") if k.strip()}


AUTH_DISABLED = os.getenv("AIDETECT_AUTH_DISABLED", "0") == "1"


# Rate limiting (valores por defecto razonables para MVP)
def get_rate_limit_requests() -> int:
    return int(os.getenv("AIDETECT_RATE_LIMIT_REQUESTS", "60"))


def get_rate_limit_window_seconds() -> int:
    return int(os.getenv("AIDETECT_RATE_LIMIT_WINDOW_SECONDS", "60"))


def is_ui_mode() -> bool:
    return os.getenv("AIDETECT_UI_MODE", "0") == "1"


def get_reports_dir() -> str | None:
    return os.getenv("AIDETECT_REPORTS_DIR") or None


def get_log_level() -> str:
    return os.getenv("AIDETECT_LOG_LEVEL", "INFO").upper()


def get_log_file() -> str | None:
    return os.getenv("AIDETECT_LOG_FILE") or None


def get_log_max_bytes() -> int:
    return int(os.getenv("AIDETECT_LOG_MAX_BYTES", str(1_000_000)))


def get_log_backup_count() -> int:
    return int(os.getenv("AIDETECT_LOG_BACKUP_COUNT", "3"))



def get_api_host() -> str:
    """
    Devuelve la dirección en la que escuchará la API.

    Por defecto usa 127.0.0.1 para desarrollo local.
    """
    return os.getenv("AIDETECT_API_HOST", "127.0.0.1")


def get_api_port() -> int:
    """
    Devuelve el puerto en el que escuchará la API.

    Por defecto usa el puerto 8000.
    """
    return int(os.getenv("AIDETECT_API_PORT", "8000"))
