
import json
import argparse
from pathlib import Path

from aidetect.text.scorer import analyze_text



def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Detector de autoría IA para texto"
    )

    subparser = parser.add_subparsers(dest="command", required=True)

    text_parser = subparser.add_parser("text", help="Analiza un archivo de texto")
    text_parser.add_argument("file", type=Path, help="Archivo de texto a analizar")
    text_parser.add_argument(
        "--output",
        type=Path,
        help="Guardar resultado en archivo JSON",
    )
    text_parser.add_argument(
        "--pretty",
        action="store_true",
        help="Salida JSON formateada",
    )
    text_parser.add_argument(
        "--verbose",
        action="store_true",
        help="Muesta información adicional",
    )

    return parser.parse_args()



def main() -> None:
    args = parse_args()

    if args.command == "text":
        if not args.file.exists():
            raise SystemExit(f"Archivo no encontrado: {args.file}")

        text = args.file.read_text(encoding="utf-8")
        result = analyze_text(text)

        data = result.__dict__

        indent = 2 if args.pretty else None
        output = json.dumps(data, indent=indent)

        if args.verbose:
            print("Análisis completado correctamente\n")

        if args.output:
            args.output.write_text(output, encoding="utf-8")
        else:
            print(output)


if __name__ == "__main__":
    main()
