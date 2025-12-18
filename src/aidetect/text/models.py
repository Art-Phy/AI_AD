
from dataclasses import dataclass
from typing import Dict


@dataclass
class TextAnalysisResult:
    """
    Resultado de análisis de un texto.

    score:
        Valor entre 0 y 1. Más alto => más probable que sea IA.
    label:
        'ai', 'human', 'uncertain'
    details:
        Métricas internas usadas para calcular el score.
    """
    score: float
    label: str
    details: Dict[str, float]
