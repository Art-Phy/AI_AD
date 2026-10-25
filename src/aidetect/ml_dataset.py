from aidetect.ml_features import feature_vector
from aidetect.ml_samples import DatasetSample


LABELS = {
    "human": 0,
    "ai": 1,
}



def encode_label(label: str) -> int:
    """
    Convierte una etiqueta textual en su representación numérica.
    """
    try:
        return LABELS[label]
    except KeyError as exc:
        raise ValueError(f"Etiqueta desconocida: {label}") from exc



def build_dataset(
    samples: list[DatasetSample],
) -> tuple[list[list[float]], list[int]]:
    """
    Construye X e y a partir de muestras etiquetadas.
    """
    X = []
    y = []

    for sample in samples:
        X.append(feature_vector(sample.text))
        y.append(encode_label(sample.label))

    return X, y
