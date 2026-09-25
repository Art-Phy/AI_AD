
import pytest

from aidetect.ml_features import (
    average_sentence_length,
    sentence_length_variance,
    punctuation_ratio,
    max_word_frequency_ratio,
    extract_features,
)
from aidetect.ml_features import FEATURE_NAMES, feature_vector



def test_average_sentence_length():
    text = "Uno dos. Uno dos tres cuatro."

    assert average_sentence_length(text) == 3.0



def test_sentence_length_variance():
    text = "Uno dos. Uno dos tres cuatro."

    assert sentence_length_variance(text) == 1.0



def test_punctuation_ratio():
    text = "Hola, mundo!"

    assert punctuation_ratio(text) == pytest.approx(2 / len(text))



def test_max_word_frequency_ratio():
    text = "perro gato perro casa"

    assert max_word_frequency_ratio(text) == 0.5



def test_extract_features_returns_expected_keys():
    features = extract_features("Hola mundo. Esto es una prueba.")

    assert set(features) == {
        "avg_sentence_length",
        "sentence_length_variance",
        "lexical_diversity",
        "punctuation_ratio",
        "max_word_frequency_ratio",
    }



def test_feature_names_have_expected_order():
    assert FEATURE_NAMES == (
        "avg_sentence_length",
        "sentence_length_variance",
        "lexical_diversity",
        "punctuation_ratio",
        "max_word_frequency_ratio",
    )



def test_feature_vector_preserves_feature_order():
    text = "perro gato perro. Esto es una prueba!"

    features = extract_features(text)
    vector = feature_vector(text)

    assert vector == [features[name] for name in FEATURE_NAMES]