
from aidetect.text.scorer import analyze_text


def test_empty_text():
    result = analyze_text("")
    assert result.label in {"human", "uncertain"}


def test_repetitive_text_looks_ai():
    text = "Hola mundo. Hola mundo. Hola mundo. Hola mundo."
    result = analyze_text(text)
    assert result.score >= 0.5


def test_natural_text_looks_human():
    text = (
        "Ayer salí a caminar sin rumbo fijo. "
        "Me encontré pensando en cosas distintas y cambiantes, "
        "como suele pasar cuando uno no tiene prisa."
    )
    result = analyze_text(text)
    assert result.label != "ai"
