
from typing import Any, Dict, Literal, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from aidetect.config import DEFAULT_MODE, MODES
from aidetect.text.scorer import analyze_text

Mode = Literal["conservative", "balanced", "aggressive"]



class AnalyzeTextRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Texto a analizar")
    mode: Optional[Mode] = Field(default=DEFAULT_MODE, description="Modo de detección")


class AnalyzeTextResponse(BaseModel):
    score: float
    label: str
    details: Dict[str, Any]



app = FastAPI(
    title="AI Authorship Detector API",
    version="0.3.0",
    description="API para estimar autoría IA en texto usando heurísticas explicables",
)

@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.get("/v1/modes")
def list_modes() -> Dict[str, Any]:
    return {
        "default": DEFAULT_MODE,
        "modes": MODES,
    }


@app.post("/v1/analyze/text", response_model=AnalyzeTextResponse)
def analyze_text_endpoint(payload: AnalyzeTextRequest) -> AnalyzeTextResponse:
    mode = payload.mode or DEFAULT_MODE

    if mode not in MODES: # Ahora mismo es innecesario, pero útil si cambia el esquema en un futuro
        raise HTTPException(status_code=400, detail=f"Unknown mode: {mode}")
    
    result = analyze_text(payload.text, mode=mode)
    return AnalyzeTextResponse(score=result.score, label=result.label, details=result.details)
