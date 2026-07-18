"""Domain models for coding-agent evaluation."""

from __future__ import annotations

from pydantic import BaseModel, Field


class Task(BaseModel):
    """A repository-level coding task an agent is asked to complete."""

    id: str
    title: str
    description: str
    allowed_paths: list[str] = Field(
        default_factory=list,
        description="Path prefixes the agent is allowed to modify; anything else is out of scope.",
    )
    test_command: str = "pytest"


class Step(BaseModel):
    """A single action in an agent trajectory (a command or tool call)."""

    index: int
    action: str  # e.g. "run", "edit", "tool_call"
    content: str


class FileChange(BaseModel):
    path: str
    status: str = "modified"  # added | modified | deleted
    added: int = 0
    removed: int = 0


class TestResult(BaseModel):
    name: str
    passed: bool


class Trajectory(BaseModel):
    """A saved agent run for a task: steps taken, files changed, tests observed."""

    task_id: str
    model: str
    steps: list[Step] = Field(default_factory=list)
    file_changes: list[FileChange] = Field(default_factory=list)
    test_results: list[TestResult] = Field(default_factory=list)
    hallucinated_imports: list[str] = Field(
        default_factory=list,
        description="Imported modules that do not exist in the environment.",
    )


class Criterion(BaseModel):
    key: str
    description: str
    weight: float = 1.0


class Rubric(BaseModel):
    criteria: list[Criterion]


class CriterionScore(BaseModel):
    key: str
    score: float  # 0..1
    weight: float
    detail: str = ""


class EvaluationReport(BaseModel):
    task_id: str
    model: str
    test_total: int
    test_passed: int
    test_pass_rate: float
    out_of_scope_files: list[str]
    hallucinated_imports: list[str]
    criteria: list[CriterionScore]
    overall_score: float  # 0..1 weighted
    rationale: str


class EvaluateRequest(BaseModel):
    task: Task
    trajectory: Trajectory
    rubric: Rubric | None = None


class CompareRequest(BaseModel):
    task: Task
    trajectory_a: Trajectory
    trajectory_b: Trajectory
    rubric: Rubric | None = None


class CompareResult(BaseModel):
    report_a: EvaluationReport
    report_b: EvaluationReport
    winner: str  # "a" | "b" | "tie"
    per_criterion_winner: dict[str, str]
