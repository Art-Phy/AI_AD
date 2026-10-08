import pytest

from aidetect.ml_dataset import build_dataset
from aidetect.ml_dataset_loader import (
    count_words,
    load_dataset_csv,
)
from aidetect.ml_samples import DatasetSample


def make_text(word_count: int) -> str:
    return " ".join(["palabra"] * word_count)



def test_count_words():
    assert count_words("Uno dos tres cuatro.") == 4



def test_load_dataset_csv(tmp_path):
    csv_file = tmp_path / "dataset.csv"

    text = make_text(120)

    csv_file.write_text(
        "id,text,label,topic,source\n"
        f'human_001,"{text}",human,running,manual\n'
        f'ai_001,"{text}",ai,running,generated\n',
        encoding="utf-8",
    )

    samples = load_dataset_csv(csv_file)

    assert samples == [
        DatasetSample(
            id="human_001",
            text=text,
            label="human",
            topic="running",
            source="manual",
        ),
        DatasetSample(
            id="ai_001",
            text=text,
            label="ai",
            topic="running",
            source="generated",
        ),
    ]



def test_load_dataset_rejects_unknown_label(tmp_path):
    csv_file = tmp_path / "dataset.csv"

    text = make_text(120)

    csv_file.write_text(
        "id,text,label,topic,source\n"
        f'unknown_001,"{text}",robot,running,test\n',
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="etiqueta desconocida"):
        load_dataset_csv(csv_file)



def test_load_dataset_rejects_duplicate_ids(tmp_path):
    csv_file = tmp_path / "dataset.csv"

    text = make_text(120)

    csv_file.write_text(
        "id,text,label,topic,source\n"
        f'sample_001,"{text}",human,running,manual\n'
        f'sample_001,"{text}",ai,running,generated\n',
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="ID duplicado"):
        load_dataset_csv(csv_file)



def test_load_dataset_rejects_short_text(tmp_path):
    csv_file = tmp_path / "dataset.csv"

    csv_file.write_text(
        "id,text,label,topic,source\n"
        'human_001,"Texto demasiado corto.",human,running,manual\n',
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="se esperaban entre"):
        load_dataset_csv(csv_file)



def test_load_dataset_rejects_missing_columns(tmp_path):
    csv_file = tmp_path / "dataset.csv"

    csv_file.write_text(
        "id,text,label\n"
        'human_001,"Texto",human\n',
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="Faltan columnas obligatorias"):
        load_dataset_csv(csv_file)



def test_ml_baseline_dataset_loads():
    samples = load_dataset_csv("data/ml_baseline.csv")
    X, y = build_dataset(samples)

    assert len(samples) > 0
    assert len(X) == len(samples)
    assert len(y) == len(samples)
    assert all(len(row) == 5 for row in X)


def test_ml_baseline_contains_both_labels():
    samples = load_dataset_csv("data/ml_baseline.csv")

    labels = {sample.label for sample in samples}

    assert labels == {"human", "ai"}
