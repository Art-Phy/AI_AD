
import os

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



def get_api_keys() -> set[str]:
    """
    Devuelve el set de API keys válidas desde la variable de entorno.

    Formato:
        AIDETECT_API_KEYS="key1key2,key3"
    """
    raw = os.getenv("AIDETECT_API_Keys", "").strip()
    if not raw:
        return set()
    return {k.strip() for k in raw.split(",") if k.strip()}


AUTH_DISABLED = os.getenv("AIDETECT_AUTH_DISABLE", "0") == "1"

# Rate limiting (valores por defecto razonables para MVP)
RATE_LIMIT_REQUESTS = int(os.getenv("AIDETECT_RATE_LIMIT_REQUESTS", "60"))
RATE_LIMIT_WINDOW_SECONDS = int(os.getenv("AIDETECT_RATE_LIMIT_WINDOW_SECONDS", "60"))
