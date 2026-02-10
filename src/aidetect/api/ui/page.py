from pathlib import Path


def render_ui_html() -> str:
    """
    Devuelve el HTML de la UI desde un archivo estático.
    """
    ui_path = Path(__file__).resolve().parent.parent / "static" / "ui.html"
    return ui_path.read_text(encoding="utf-8")

