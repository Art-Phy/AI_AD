
import pytest

from aidetect.ml_dataset import LABELS, build_dataset, encode_label
from aidetect.ml_features import feature_vector
from aidetect.ml_samples import DatasetSample



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
        DatasetSample(
            id="human_001",
            text="Hola mundo. Esto es humano.",
            label="human",
            topic="test",
            source="test",
        ),
        DatasetSample(
            id="ai_001",
            text="Texto generado para una prueba.",
            label="ai",
            topic="test",
            source="test",
        ),
    ]

    X, y = build_dataset(samples)

    assert X == [
        feature_vector(samples[0].text),
        feature_vector(samples[1].text),
    ]

    assert y == [0, 1]



def test_build_dataset_empty():
    X, y = build_dataset([])

    assert X == []
    assert y == []
