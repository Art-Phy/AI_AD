
import re
from collections import Counter



def sentence_lengths(text: str) -> list[int]:
    """
    Devuelve la longitud de cada frase (en palabras).
    """
    sentences = re.split(r"[.!?]+", text)
    return [len(s.split()) for s in sentences if s.strip()]



def sentence_uniformity(text: str) -> float:
    """
    Mide lo similares que son las longitudes de las frases.

    IA tiende a generar frases con longitudes más uniformes.
    Valor entre 0 y 1 (1 = muy uniforme).
    """
    lengths = sentence_lengths(text)
    if len(lengths) < 2:
        return 0.0
    
    avg = sum(lengths) / len(lengths)
    variance = sum((l - avg) ** 2 for l in lengths) / len(lengths)

    # Normalizamos de forma simple
    return 1 / (1 + variance)



def repetition_score(text: str) -> float:
    """
    Detecta repetición de palabras.

    IA tiende a repetir estructuras y términos
    """
    words = re.findall(r"\b\w+\b", text.lower())
    if not words:
        return 0.0
    
    counts = Counter(words)
    most_common = counts.most_common(1)[0][1]

    return most_common / len(words)



def lexical_diversity(text: str) -> float:
    """
    Ratio de palabras únicas respecto al total.
    Valor entre 0 y 1.
    """
    words = re.findall(r"\b\w+\b", text.lower())
    if not words:
        return 0.0
    
    return len(set(words)) / len(words)



def average_word_length(text: str) -> float:
    """
    Longitud media de las palabras
    """
    words = re.findall(r"\b\w+\b", text)
    if not words:
        return 0.0
    
    return sum(len(w) for w in words) / len(words)



def long_word_ratio(text: str, threshold: int = 7) -> float:
    """
    Proporción de palabras largas (>= threshold)
    """
    words = re.findall(r"\b\w+\b", text)
    if not words:
        return 0.0
    
    long_word = [w for w in words if len(w) >= threshold]
    return len(long_word) / len(words)
