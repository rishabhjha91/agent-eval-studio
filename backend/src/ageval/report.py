"""Render an EvaluationReport as JSON or a small standalone HTML page."""

from __future__ import annotations

import html
import json

from .models import EvaluationReport


def to_json(report: EvaluationReport) -> str:
    return json.dumps(report.model_dump(), indent=2)


def to_html(report: EvaluationReport) -> str:
    rows = "\n".join(
        f"<tr><td>{html.escape(c.key)}</td>"
        f"<td>{c.score:.2f}</td>"
        f"<td>{c.weight:.1f}</td>"
        f"<td>{html.escape(c.detail)}</td></tr>"
        for c in report.criteria
    )
    oos = ", ".join(html.escape(p) for p in report.out_of_scope_files) or "none"
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>AgentEval report - {html.escape(report.task_id)}</title>
<style>
  body {{ font-family: system-ui, Arial, sans-serif; margin: 24px; color: #1c1c1c; }}
  h1 {{ font-size: 20px; }}
  .overall {{ font-size: 28px; font-weight: 700; color: #0f2b46; }}
  table {{ border-collapse: collapse; margin-top: 12px; width: 100%; }}
  th, td {{ border: 1px solid #ccc; padding: 6px 10px; text-align: left; font-size: 14px; }}
  th {{ background: #f2f5f8; }}
  .rationale {{ margin-top: 12px; padding: 10px; background: #f7f9fb; border-left: 3px solid #0f2b46; }}
</style>
</head>
<body>
  <h1>AgentEval Studio - {html.escape(report.task_id)} ({html.escape(report.model)})</h1>
  <div class="overall">Overall: {report.overall_score:.2f}</div>
  <p>Tests: {report.test_passed}/{report.test_total} passed
     ({report.test_pass_rate:.0%}) &nbsp;|&nbsp; Out-of-scope files: {oos}</p>
  <table>
    <thead><tr><th>Criterion</th><th>Score</th><th>Weight</th><th>Detail</th></tr></thead>
    <tbody>
{rows}
    </tbody>
  </table>
  <div class="rationale">{html.escape(report.rationale)}</div>
</body>
</html>
"""
