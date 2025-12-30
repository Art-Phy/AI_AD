
from aidetect.config import MODES, DEFAULT_MODE
from aidetect.text.analyzer import (
    sentence_uniformity,
    repetition_score,
    lexical_diversity,
    average_word_length,
    long_word_ratio,
)
from aidetect.text.models import TextAnalysisResult



def classify_score(score: float, mode: str) -> str:
    if mode not in MODES:
        raise ValueError(f"Modo desconocido: {mode}")
    
    thresholds = MODES[mode]

    if score >= thresholds["ai_threshold"]:
        return "ai"
    if score <= thresholds["human_threshold"]:
        return "human"
    return "uncertain"



def analyze_text(text: str, mode: str = DEFAULT_MODE) -> TextAnalysisResult:
    """
    Analiza un texto y devuelve una estimación de autoría.

    El score final es una combinación ponderada de heurísticas.
    """
    uniformity = sentence_uniformity(text)
    repetition = repetition_score(text)
    diversity = lexical_diversity(text)
    avg_word_len = average_word_length(text)
    long_words = long_word_ratio(text)

    # Normalizaciones simples
    norm_avg_word_len = min(avg_word_len / 10, 1.0)

    # Score combinado
    score = (
        0.25 * uniformity +
        0.25 * repetition +
        0.20 * (1 - diversity) +
        0.15 * norm_avg_word_len +
        0.15 * long_words
    )

    label = classify_score(score, mode)

    return TextAnalysisResult(
        score=round(score, 3),
        label=label,
        details={
            "mode": mode,
            "sentence_uniformity": round(uniformity, 3),
            "repetition_score": round(repetition, 3),
            "lexical_diversity": round(diversity, 3),
            "avg_word_length": round(avg_word_len, 3),
            "long_word_ratio": round(long_words, 3),
        },
    )
