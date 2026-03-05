
from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from logging.handlers import RotatingFileHandler
from typing import Any, Dict, Optional

from aidetect.config import (
    get_log_backup_count,
    get_log_file,
    get_log_level,
    get_log_max_bytes,
)


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload: Dict[str, Any] = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "event": record.getMessage(),
        }

        # Incluye extra fields por si hace falta (request_id, path, etc.)
        for key in ("request_id", "method", "path", "status_code", "elapsed_ms"):
            if hasattr(record, key):
                payload[key] = getattr(record, key)

        if record.exc_info:
            payload["exc"] = self.formatException(record.exc_info)

        return json.dumps(payload, ensure_ascii=False)
    


def setup_logging() -> None:
    level = get_log_level()
    log_file: Optional[str] = get_log_file()

    logger = logging.getLogger()
    logger.setLevel(level)
    logger.handlers.clear()

    formatter = JsonFormatter()

    # Consola
    sh = logging.StreamHandler()
    sh.setFormatter(formatter)
    logger.addHandler(sh)

    # Fichero rotativo (opcional)
    if log_file:
        fh = RotatingFileHandler(
            log_file,
            maxBytes=get_log_max_bytes(),
            backupCount=get_log_backup_count(),
            encoding="utf-8",
        )
        fh.setFormatter(formatter)
        logger.addHandler(fh)
