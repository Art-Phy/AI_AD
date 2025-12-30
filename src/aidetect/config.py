
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
