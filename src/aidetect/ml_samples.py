from dataclasses import dataclass


@dataclass(frozen=True)
class DatasetSample:
    id: str
    text: str
    label: str
    topic: str
    source: str
