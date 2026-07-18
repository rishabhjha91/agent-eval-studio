import type { EvaluationReport } from "../types";
import { ScoreBar } from "./ScoreBar";

interface EvaluationCardProps {
  report: EvaluationReport;
  highlight?: boolean;
}

export function EvaluationCard({ report, highlight }: EvaluationCardProps) {
  return (
    <section
      className={`eval-card${highlight ? " eval-card--winner" : ""}`}
      data-testid={`eval-card-${report.model}`}
    >
      <header className="eval-card__header">
        <h3>{report.model}</h3>
        <span className="eval-card__overall">{report.overall_score.toFixed(2)}</span>
      </header>

      <p className="eval-card__tests">
        Tests: {report.test_passed}/{report.test_total} (
        {Math.round(report.test_pass_rate * 100)}%)
      </p>

      <div className="eval-card__criteria">
        {report.criteria.map((c) => (
          <ScoreBar key={c.key} label={c.key} score={c.score} detail={c.detail} />
        ))}
      </div>

      {report.out_of_scope_files.length > 0 && (
        <div className="eval-card__flag" data-testid="out-of-scope">
          <strong>Out of scope:</strong> {report.out_of_scope_files.join(", ")}
        </div>
      )}

      {report.hallucinated_imports.length > 0 && (
        <div className="eval-card__flag" data-testid="hallucinated">
          <strong>Hallucinated imports:</strong>{" "}
          {report.hallucinated_imports.join(", ")}
        </div>
      )}

      <p className="eval-card__rationale">{report.rationale}</p>
    </section>
  );
}
