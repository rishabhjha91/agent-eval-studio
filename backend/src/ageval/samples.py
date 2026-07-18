"""Reproducible sample task and trajectories (no network, no model API required).

These emulate a saved coding-agent run so the studio is demonstrable offline:
one "good" trajectory that fixes the bug within scope, and one "bad" trajectory
that edits out-of-scope files, hallucinates an import, and fails tests.
"""

from __future__ import annotations

from .models import FileChange, Step, Task, TestResult, Trajectory

SAMPLE_TASK = Task(
    id="fix-discount-rounding",
    title="Fix rounding bug in order-total discount",
    description=(
        "The checkout total applies a percentage discount but rounds incorrectly, "
        "producing off-by-one-cent totals. Fix the rounding in the pricing module "
        "and make the failing tests pass without changing the public API."
    ),
    allowed_paths=["src/pricing/", "tests/"],
    test_command="pytest tests/test_pricing.py",
)

GOOD_TRAJECTORY = Trajectory(
    task_id="fix-discount-rounding",
    model="agent-good",
    steps=[
        Step(index=0, action="run", content="pytest -q tests/test_pricing.py"),
        Step(index=1, action="read", content="open src/pricing/discount.py"),
        Step(index=2, action="edit", content="use Decimal.quantize with ROUND_HALF_UP"),
        Step(index=3, action="run", content="pytest -q tests/test_pricing.py"),
    ],
    file_changes=[
        FileChange(path="src/pricing/discount.py", status="modified", added=6, removed=3),
    ],
    test_results=[
        TestResult(name="test_no_discount", passed=True),
        TestResult(name="test_ten_percent", passed=True),
        TestResult(name="test_rounding_half_up", passed=True),
        TestResult(name="test_full_discount", passed=True),
    ],
    hallucinated_imports=[],
)

BAD_TRAJECTORY = Trajectory(
    task_id="fix-discount-rounding",
    model="agent-bad",
    steps=[
        Step(index=0, action="run", content="pytest -q"),
        Step(index=1, action="edit", content="import moneyfmt  # not installed"),
        Step(index=2, action="edit", content="patch discount.py"),
        Step(index=3, action="edit", content="edit src/billing/invoice.py (unrelated)"),
        Step(index=4, action="edit", content="edit README.md"),
        Step(index=5, action="run", content="pytest -q"),
    ],
    file_changes=[
        FileChange(path="src/pricing/discount.py", status="modified", added=4, removed=2),
        FileChange(path="src/billing/invoice.py", status="modified", added=10, removed=1),
        FileChange(path="README.md", status="modified", added=2, removed=0),
    ],
    test_results=[
        TestResult(name="test_no_discount", passed=True),
        TestResult(name="test_ten_percent", passed=False),
        TestResult(name="test_rounding_half_up", passed=False),
        TestResult(name="test_full_discount", passed=True),
    ],
    hallucinated_imports=["moneyfmt"],
)
