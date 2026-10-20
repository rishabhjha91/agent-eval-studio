"""Scoring engine: turn a task + trajectory into a structured evaluation report.

The rubric criteria mirror what a human coding-agent evaluator looks at:
correctness (tests), scope control (did it only touch allowed files), grounding
(no hallucinated imports), and efficiency (reasonable number of steps). Each
criterion is scored in 0..1 from concrete trajectory signals so the result is
deterministic and reproducible; the weighted mean gives the overall score.
"""

from __future__ import annotations

from .models import (
    CompareResult,
    Criterion,
    CriterionScore,
    EvaluationReport,
    Rubric,
    Task,
    Trajectory,
)

DEFAULT_RUBRIC = Rubric(
    criteria=[
        Criterion(key="correctness", description="Fraction of tests passing", weight=3.0),
        Criterion(key="scope_control", description="Changes stay within allowed paths", weight=1.5),
        Criterion(key="grounding", description="No hallucinated / nonexistent imports", weight=1.5),
        Criterion(key="efficiency", description="Reasonable number of steps for the change", weight=1.0),
    ]
)

# Above this many steps, efficiency starts to degrade linearly to 0 at 3x.
EFFICIENCY_BASELINE_STEPS = 12


def _path_allowed(path: str, allowed: list[str]) -> bool:
    """Return whether a changed path matches an allowed path or prefix.

    Directory prefixes must end at a path boundary. An explicit trailing
    ``*`` retains the original behavior of matching any string prefix.
    """
    if not allowed:
        return True

    for entry in allowed:
        prefix = entry.rstrip("*")

        if entry.endswith("*"):
            if path.startswith(prefix):
                return True
        elif prefix.endswith("/"):
            if path.startswith(prefix):
                return True
        elif path == prefix or path.startswith(prefix + "/"):
            return True

    return False


def out_of_scope_files(task: Task, trajectory: Trajectory) -> list[str]:
    return [
        fc.path
        for fc in trajectory.file_changes
        if not _path_allowed(fc.path, task.allowed_paths)
    ]


def test_stats(trajectory: Trajectory) -> tuple[int, int, float]:
    total = len(trajectory.test_results)
    passed = sum(1 for t in trajectory.test_results if t.passed)
    rate = passed / total if total else 0.0
    return total, passed, rate


def _efficiency_score(n_steps: int) -> float:
    if n_steps <= EFFICIENCY_BASELINE_STEPS:
        return 1.0
    over = n_steps - EFFICIENCY_BASELINE_STEPS
    return max(0.0, 1.0 - over / (2 * EFFICIENCY_BASELINE_STEPS))


def evaluate(task: Task, trajectory: Trajectory, rubric: Rubric | None = None) -> EvaluationReport:
    rubric = rubric or DEFAULT_RUBRIC
    total, passed, rate = test_stats(trajectory)
    oos = out_of_scope_files(task, trajectory)
    n_changed = len(trajectory.file_changes) or 1

    signals = {
        "correctness": rate,
        "scope_control": max(0.0, 1.0 - len(oos) / n_changed),
        "grounding": 0.0 if trajectory.hallucinated_imports else 1.0,
        "efficiency": _efficiency_score(len(trajectory.steps)),
    }
    details = {
        "correctness": f"{passed}/{total} tests passed",
        "scope_control": f"{len(oos)} of {n_changed} changed files out of scope",
        "grounding": (
            "hallucinated: " + ", ".join(trajectory.hallucinated_imports)
            if trajectory.hallucinated_imports
            else "no hallucinated imports"
        ),
        "efficiency": f"{len(trajectory.steps)} steps",
    }

    scores: list[CriterionScore] = []
    weighted_sum = 0.0
    weight_total = 0.0
    for c in rubric.criteria:
        s = float(signals.get(c.key, 0.0))
        scores.append(CriterionScore(key=c.key, score=round(s, 3), weight=c.weight, detail=details.get(c.key, "")))
        weighted_sum += s * c.weight
        weight_total += c.weight

    overall = round(weighted_sum / weight_total, 3) if weight_total else 0.0

    return EvaluationReport(
        task_id=task.id,
        model=trajectory.model,
        test_total=total,
        test_passed=passed,
        test_pass_rate=round(rate, 3),
        out_of_scope_files=oos,
        hallucinated_imports=trajectory.hallucinated_imports,
        criteria=scores,
        overall_score=overall,
        rationale=_rationale(rate, oos, trajectory),
    )


def _rationale(rate: float, oos: list[str], trajectory: Trajectory) -> str:
    parts: list[str] = []
    if rate == 1.0:
        parts.append("All tests pass.")
    elif rate == 0.0:
        parts.append("No tests pass; the change does not solve the task.")
    else:
        parts.append(f"Partial fix: {round(rate * 100)}% of tests pass.")
    if oos:
        parts.append(f"Modifies {len(oos)} file(s) outside the allowed scope ({', '.join(oos)}).")
    else:
        parts.append("Changes stay within the allowed scope.")
    if trajectory.hallucinated_imports:
        parts.append(
            "Uses imports that do not exist in the environment: "
            + ", ".join(trajectory.hallucinated_imports)
            + "."
        )
    return " ".join(parts)


def compare(
    task: Task,
    trajectory_a: Trajectory,
    trajectory_b: Trajectory,
    rubric: Rubric | None = None,
) -> CompareResult:
    rubric = rubric or DEFAULT_RUBRIC
    ra = evaluate(task, trajectory_a, rubric)
    rb = evaluate(task, trajectory_b, rubric)

    per_criterion: dict[str, str] = {}
    a_by_key = {c.key: c.score for c in ra.criteria}
    b_by_key = {c.key: c.score for c in rb.criteria}
    for key in a_by_key:
        av, bv = a_by_key[key], b_by_key.get(key, 0.0)
        per_criterion[key] = "a" if av > bv else "b" if bv > av else "tie"

    if ra.overall_score > rb.overall_score:
        winner = "a"
    elif rb.overall_score > ra.overall_score:
        winner = "b"
    else:
        winner = "tie"

    return CompareResult(
        report_a=ra,
        report_b=rb,
        winner=winner,
        per_criterion_winner=per_criterion,
    )
