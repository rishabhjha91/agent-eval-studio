export interface CriterionScore {
  key: string;
  score: number;
  weight: number;
  detail: string;
}

export interface EvaluationReport {
  task_id: string;
  model: string;
  test_total: number;
  test_passed: number;
  test_pass_rate: number;
  out_of_scope_files: string[];
  hallucinated_imports: string[];
  criteria: CriterionScore[];
  overall_score: number;
  rationale: string;
}

export interface CompareResult {
  report_a: EvaluationReport;
  report_b: EvaluationReport;
  winner: "a" | "b" | "tie";
  per_criterion_winner: Record<string, string>;
}
