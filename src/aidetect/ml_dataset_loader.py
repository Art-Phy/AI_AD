import csv
import re
from pathlib import Path

from aidetect.ml_dataset import LABELS
from aidetect.ml_samples import DatasetSample


REQUIRED_COLUMNS = {
    "id",
    "text",
    "label",
    "topic",
    "source",
}

MIN_WORDS = 120
MAX_WORDS = 300


def count_words(text: str) -> int:
    """
    Cuenta las palabras de una muestra.
    """
    return len(re.findall(r"\b\w+\b", text))


def validate_sample(sample: DatasetSample) -> None:
    """
    Valida una muestra antes de incorporarla al dataset.
    """
    if not sample.id.strip():
        raise ValueError("La muestra no puede tener un id vacío")

    if not sample.text.strip():
        raise ValueError(f"La muestra {sample.id} tiene el texto vacío")

    if sample.label not in LABELS:
        raise ValueError(
            f"La muestra {sample.id} tiene una etiqueta desconocida: {sample.label}"
        )

    if not sample.topic.strip():
        raise ValueError(f"La muestra {sample.id} no tiene topic")

    if not sample.source.strip():
        raise ValueError(f"La muestra {sample.id} no tiene source")

    word_count = count_words(sample.text)

    if not MIN_WORDS <= word_count <= MAX_WORDS:
        raise ValueError(
            f"La muestra {sample.id} tiene {word_count} palabras; "
            f"se esperaban entre {MIN_WORDS} y {MAX_WORDS}"
        )


def load_dataset_csv(path: str | Path) -> list[DatasetSample]:
    """
    Carga y valida muestras desde un fichero CSV.
    """
    path = Path(path)

    samples = []
    seen_ids = set()

    with path.open("r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)

        if reader.fieldnames is None:
            raise ValueError("El CSV no contiene cabecera")

        missing_columns = REQUIRED_COLUMNS - set(reader.fieldnames)

        if missing_columns:
            missing = ", ".join(sorted(missing_columns))
            raise ValueError(f"Faltan columnas obligatorias: {missing}")

        for row in reader:
            sample = DatasetSample(
                id=row["id"].strip(),
                text=row["text"].strip(),
                label=row["label"].strip().lower(),
                topic=row["topic"].strip(),
                source=row["source"].strip(),
            )

            if sample.id in seen_ids:
                raise ValueError(f"ID duplicado: {sample.id}")

            validate_sample(sample)

            seen_ids.add(sample.id)
            samples.append(sample)

    return samples
