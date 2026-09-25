
import re
from collections import Counter

from aidetect.text.analyzer import sentence_lengths, lexical_diversity



def average_sentence_length(text: str) -> float:
    """Longitud media de las frases, medida en palabras"""
    lengths = sentence_lengths(text)

    if not lengths:
        return 0.0

    return sum(lengths) / len(lengths)



def sentence_length_variance(text: str) -> float:
    """Varianza de la longitud de las frases"""
    lengths = sentence_lengths(text)

    if len(lengths) < 2:
        return 0.0

    avg = sum(lengths) / len(lengths)

    return sum((length - avg) ** 2 for length in lengths) / len(lengths)



def punctuation_ratio(text: str) -> float:
    """Proporción de signos de puntuación respecto al total de caracteres"""
    if not text:
        return 0.0

    punctuation = re.findall(r"[.,;:!?]", text)

    return len(punctuation) / len(text)



def max_word_frequency_ratio(text: str) -> float:
    """Proporción correspondiente a la palabra más frecuente del texto"""
    words = re.findall(r"\b\w+\b", text.lower())

    if not words:
        return 0.0

    counts = Counter(words)
    most_common_count = counts.most_common(1)[0][1]

    return most_common_count / len(words)



def extract_features(text: str) -> dict[str, float]:
    """Extrae el Feature Set v1 utilizado por el baseline de ML"""
    return {
        "avg_sentence_length": average_sentence_length(text),
        "sentence_length_variance": sentence_length_variance(text),
        "lexical_diversity": lexical_diversity(text),
        "punctuation_ratio": punctuation_ratio(text),
        "max_word_frequency_ratio": max_word_frequency_ratio(text),
    }
