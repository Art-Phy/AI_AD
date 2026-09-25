
import pytest

from aidetect.ml_dataset import LABELS, build_dataset, encode_label
from aidetect.ml_features import feature_vector



def test_label_mapping():
    assert LABELS == {
        "human": 0,
        "ai": 1,
    }



def test_encode_label():
    assert encode_label("human") == 0
    assert encode_label("ai") == 1



def test_encode_label_rejects_unknown_label():
    with pytest.raises(ValueError, match="Etiqueta desconocida"):
        encode_label("unknown")



def test_build_dataset():
    samples = [
        ("Hola mundo. Esto es humano.", "human"),
        ("Texto generado para una prueba.", "ai"),
    ]

    X, y = build_dataset(samples)

    assert X == [
        feature_vector(samples[0][0]),
        feature_vector(samples[1][0]),
    ]

    assert y == [0, 1]



def test_build_dataset_empty():
    X, y = build_dataset([])

    assert X == []
    assert y == []
