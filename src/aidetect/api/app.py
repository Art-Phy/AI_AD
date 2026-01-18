
from dotenv import load_dotenv
load_dotenv()
from typing import Any, Dict, Literal, Optional

from fastapi import FastAPI, Request
from pydantic import BaseModel, Field

from aidetect.config import (
    DEFAULT_MODE,
    MODES,
    RATE_LIMIT_REQUESTS,
    RATE_LIMIT_WINDOW_SECONDS,
)
from aidetect.text.scorer import analyze_text
from aidetect.api.security import require_api_key
from aidetect.api.rate_limit import InMemoryRateLimiter

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
    version="0.4.0",
    description="API para estimar la autoría IA en texto usando heurísticas explicables.",
)

# Singleton por proceso (MVP). Se resetea al reiniciar.
limiter = InMemoryRateLimiter(
    max_requests=RATE_LIMIT_REQUESTS,
    window_seconds=RATE_LIMIT_WINDOW_SECONDS,
)


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.get("/v1/modes")
def list_modes(request: Request) -> Dict[str, Any]:
    api_key = require_api_key(request)
    limiter.check(api_key)
    return {"default": DEFAULT_MODE, "modes": MODES}


@app.post("/v1/analyze/text", response_model=AnalyzeTextResponse)
def analyze_text_endpoint(payload: AnalyzeTextRequest, request: Request) -> AnalyzeTextResponse:
    api_key = require_api_key(request)
    limiter.check(api_key)

    result = analyze_text(payload.text, mode=payload.mode)
    return AnalyzeTextResponse(score=result.score, label=result.label, details=result.details)
