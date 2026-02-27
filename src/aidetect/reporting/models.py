
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, Optional



@dataclass(frozen=True)
class TextAnalysisReport:
    generated_at: str
    request_id: Optional[str]
    input: Dict[str, Any]
    result: Dict[str, Any]

    @staticmethod
    def now_iso() -> str:
        return datetime.now(timezone.utc).isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "generated_at": self.generated_at,
            "request_id": self.request_id,
            "input": self.input,
            "result": self.result,
        }
