"""FastAPI service exposing the evaluation engine."""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from . import __version__, report, samples, scoring
from .models import (
    CompareRequest,
    CompareResult,
    EvaluateRequest,
    EvaluationReport,
)

app = FastAPI(title="AgentEval Studio", version=__version__)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "version": __version__}


@app.get("/sample", response_model=CompareResult)
def sample() -> CompareResult:
    """Return a ready-made comparison of the built-in good vs. bad trajectory."""
    return scoring.compare(samples.SAMPLE_TASK, samples.GOOD_TRAJECTORY, samples.BAD_TRAJECTORY)


@app.post("/evaluate", response_model=EvaluationReport)
def evaluate(req: EvaluateRequest) -> EvaluationReport:
    return scoring.evaluate(req.task, req.trajectory, req.rubric)


@app.post("/evaluate/html", response_class=HTMLResponse)
def evaluate_html(req: EvaluateRequest) -> HTMLResponse:
    rep = scoring.evaluate(req.task, req.trajectory, req.rubric)
    return HTMLResponse(content=report.to_html(rep))


@app.post("/compare", response_model=CompareResult)
def compare(req: CompareRequest) -> CompareResult:
    return scoring.compare(req.task, req.trajectory_a, req.trajectory_b, req.rubric)
