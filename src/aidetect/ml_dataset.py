
from aidetect.ml_features import feature_vector


LABELS = {
    "human": 0,
    "ai": 1,
}



def encode_label(label: str) -> int:
    """Convierte una etiqueta textual en su representación numérica"""
    try:
        return LABELS[label]
    except KeyError as exc:
        raise ValueError(f"Etiqueta desconocida: {label}") from exc



def build_dataset(samples: list[tuple[str, str]]) -> tuple[list[list[float]], list[int]]:
    """Construye X e y a partir de pares (texto, etiqueta)"""
    X = []
    y = []

    for text, label in samples:
        X.append(feature_vector(text))
        y.append(encode_label(label))

    return X, y
