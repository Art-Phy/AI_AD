
from aidetect.text.analyzer import sentence_uniformity, repetition_score
from aidetect.text.models import TextAnalysisResult



def analyze_text(text: str) -> TextAnalysisResult:
    """
    Analiza un texto y devuelve una estimación de autoría.

    El score final es una combinación ponderada de heurísticas.
    """
    uniformity = sentence_uniformity(text)
    repetition = repetition_score(text)

    # Pesos iniciales (experimentales)
    score = (0.6 * uniformity) + (0.4 * repetition)

    if score > 0.7:
        label = "ai"
    elif score < 0.4:
        label = "human"
    else:
        label = "uncertain"

    return TextAnalysisResult(
        score=round(score, 3),
        label=label,
        details={
            "sentence_uniformity": round(uniformity, 3),
            "repetition_score": round(repetition, 3)
        }
    )
