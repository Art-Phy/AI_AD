
import logging
from dotenv import load_dotenv
load_dotenv()
from typing import Any, Dict, Literal, Optional
from pathlib import Path

from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi import FastAPI, Request
from pydantic import BaseModel, Field

from aidetect.config import (
    DEFAULT_MODE,
    MODES,
    get_rate_limit_requests,
    get_rate_limit_window_seconds,
)

from aidetect.api.middleware import RequestLoggingMiddleware
from aidetect.text.scorer import analyze_text
from aidetect.api.security import require_api_key
from aidetect.api.rate_limit import InMemoryRateLimiter
from aidetect.api.ui.page import render_ui_html
from aidetect.__about__ import __version__

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

app.add_middleware(RequestLoggingMiddleware)

static_dir = Path(__file__).resolve().parent / "static"
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Singleton por proceso (MVP). Se resetea al reiniciar.
limiter = InMemoryRateLimiter(
    max_requests=get_rate_limit_requests(),
    window_seconds=get_rate_limit_window_seconds(),
)

logging.basicConfig(level=logging.INFO)

@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.get("/ui", response_class=HTMLResponse)
def ui() -> str:
    return render_ui_html()


@app.get("/version")
def version() -> dict[str, str]:
    return{"version": __version__}


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
