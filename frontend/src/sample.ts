import type { CompareResult } from "./types";

// Mirrors the backend /sample response so the UI is demonstrable offline
// (and so tests do not depend on a running server).
export const SAMPLE_COMPARISON: CompareResult = {
  winner: "a",
  per_criterion_winner: {
    correctness: "a",
    scope_control: "a",
    grounding: "a",
    efficiency: "tie",
  },
  report_a: {
    task_id: "fix-discount-rounding",
    model: "agent-good",
    test_total: 4,
    test_passed: 4,
    test_pass_rate: 1.0,
    out_of_scope_files: [],
    hallucinated_imports: [],
    overall_score: 1.0,
    rationale:
      "All tests pass. Changes stay within the allowed scope.",
    criteria: [
      { key: "correctness", score: 1.0, weight: 3.0, detail: "4/4 tests passed" },
      { key: "scope_control", score: 1.0, weight: 1.5, detail: "0 of 1 changed files out of scope" },
      { key: "grounding", score: 1.0, weight: 1.5, detail: "no hallucinated imports" },
      { key: "efficiency", score: 1.0, weight: 1.0, detail: "4 steps" },
    ],
  },
  report_b: {
    task_id: "fix-discount-rounding",
    model: "agent-bad",
    test_total: 4,
    test_passed: 2,
    test_pass_rate: 0.5,
    out_of_scope_files: ["src/billing/invoice.py", "README.md"],
    hallucinated_imports: ["moneyfmt"],
    overall_score: 0.376,
    rationale:
      "Partial fix: 50% of tests pass. Modifies 2 file(s) outside the allowed scope (src/billing/invoice.py, README.md). Uses imports that do not exist in the environment: moneyfmt.",
    criteria: [
      { key: "correctness", score: 0.5, weight: 3.0, detail: "2/4 tests passed" },
      { key: "scope_control", score: 0.333, weight: 1.5, detail: "2 of 3 changed files out of scope" },
      { key: "grounding", score: 0.0, weight: 1.5, detail: "hallucinated: moneyfmt" },
      { key: "efficiency", score: 1.0, weight: 1.0, detail: "6 steps" },
    ],
  },
};
