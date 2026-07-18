# AgentEval Studio

A small **full-stack coding-agent evaluation tool**. It takes a saved agent
trajectory for a repository task and scores it against a rubric - correctness
(tests), scope control (only allowed files touched), grounding (no hallucinated
imports), and efficiency (step count) - then renders the result and lets you
compare two model runs side by side.

- **Backend:** Python, FastAPI, Pydantic v2, pytest.
- **Frontend:** React, TypeScript, Vite, Vitest + Testing Library.
- **Reproducible:** ships a sample task with a "good" and a "bad" trajectory, so
  it runs fully offline with no model API keys.

```
+-----------------------------+        +-----------------------------------+
|  React + TS frontend        |  HTTP  |  FastAPI backend (ageval)         |
|  - compare panel            | <----> |  /health  /sample                 |
|  - per-criterion score bars |        |  /evaluate  /evaluate/html        |
|  - scope / hallucination    |        |  /compare                         |
|    flags                    |        |  scoring engine + JSON/HTML report|
+-----------------------------+        +-----------------------------------+
```

## What it demonstrates

Coding-agent / code-QA evaluation, rubric scoring, out-of-scope-change detection,
hallucinated-import detection, run-vs-run comparison, REST API design, Pydantic
schemas, pytest, React component design with state/loading/error handling,
TypeScript, and Vitest testing.

## Backend

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
ruff check . && pytest
uvicorn ageval.api:app --reload   # http://localhost:8000/docs
```

Key endpoints:

| Method | Path | Purpose |
| --- | --- | --- |
| GET | `/health` | Liveness check |
| GET | `/sample` | Built-in good-vs-bad comparison |
| POST | `/evaluate` | Score one trajectory -> JSON report |
| POST | `/evaluate/html` | Score one trajectory -> HTML report |
| POST | `/compare` | Score and compare two trajectories |

## Frontend

```bash
cd frontend
npm install
npm run test      # Vitest + Testing Library
npm run build     # type-check + production build
npm run dev       # http://localhost:5173
```

The UI renders bundled sample data by default and has a **Load from API** button
that calls the backend `/sample` endpoint (set `VITE_API_URL` to point elsewhere).

## Scoring model

Each criterion is derived deterministically from trajectory signals and scored in
`0..1`; the overall score is the weight-normalised mean. Defaults:

| Criterion | Weight | Signal |
| --- | --- | --- |
| correctness | 3.0 | fraction of tests passing |
| scope_control | 1.5 | `1 - out_of_scope / changed_files` |
| grounding | 1.5 | `0` if any hallucinated import else `1` |
| efficiency | 1.0 | full up to a step baseline, then decays |

Weights and criteria are configurable per request via the `rubric` field.

## Layout

```
backend/
  src/ageval/{models,scoring,report,samples,api}.py
  tests/{test_scoring,test_api}.py
frontend/
  src/{App,api,sample,types}.tsx
  src/components/{ComparePanel,EvaluationCard,ScoreBar}.tsx
  src/__tests__/ComparePanel.test.tsx
.github/workflows/ci.yml
```

## License

MIT
