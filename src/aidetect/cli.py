
import json
import sys
from pathlib import Path

from aidetect.text.scorer import analyze_text



def main() -> None:
    """
    Punto de entrada del CLI
    """
    if len(sys.argv) < 3 or sys.argv[1] != "text":
        print("Uso: python -m aidetect text <archivo.txt>")
        sys.exit(1)

    file_path = Path(sys.argv[2])

    if not file_path.exists():
        print(f"Archivo no encontrado: {file_path}")
        sys.exit(1)

    text = file_path.read_text(encoding="utf-8")

    result = analyze_text(text)

    print(json.dumps(result.__dict__, indent=2))


if __name__ == "__main__":
    main()
