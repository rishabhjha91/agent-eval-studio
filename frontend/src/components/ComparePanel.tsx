import type { CompareResult } from "../types";
import { EvaluationCard } from "./EvaluationCard";

interface ComparePanelProps {
  result: CompareResult;
}

const WINNER_LABEL: Record<string, string> = {
  a: "Model A wins",
  b: "Model B wins",
  tie: "Tie",
};

export function ComparePanel({ result }: ComparePanelProps) {
  return (
    <div className="compare-panel">
      <div className="compare-panel__verdict" data-testid="verdict">
        {WINNER_LABEL[result.winner]}
      </div>
      <div className="compare-panel__grid">
        <EvaluationCard report={result.report_a} highlight={result.winner === "a"} />
        <EvaluationCard report={result.report_b} highlight={result.winner === "b"} />
      </div>
    </div>
  );
}
