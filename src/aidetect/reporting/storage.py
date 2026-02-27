
from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from aidetect.reporting.models import TextAnalysisReport



def save_report(report: TextAnalysisReport, reports_dir: Optional[str]) -> Optional[Path]:
    """
    Guarda el reporte en disco si reports_dir está configurado.
    Devuelve la ruta del archivo guardado o None si no se guarda.
    """
    if not reports_dir:
        return None
    
    base = Path(reports_dir).expanduser().resolve()
    base.mkdir(parents=True, exist_ok=True)

    ts_safe = report.generated_at.replace(":", "-").replace(".", "-")
    filename = f"aidetect-report-{ts_safe}.json"
    path = base / filename

    path.write_text(json.dumps(report.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")
    return path
