interface ScoreBarProps {
  label: string;
  score: number;
  detail?: string;
}

function colorFor(score: number): string {
  if (score >= 0.8) return "#1f8a4c";
  if (score >= 0.5) return "#c98a00";
  return "#c0392b";
}

export function ScoreBar({ label, score, detail }: ScoreBarProps) {
  const pct = Math.round(score * 100);
  return (
    <div className="score-bar" data-testid={`score-${label}`}>
      <div className="score-bar__head">
        <span className="score-bar__label">{label}</span>
        <span className="score-bar__value">{score.toFixed(2)}</span>
      </div>
      <div className="score-bar__track">
        <div
          className="score-bar__fill"
          style={{ width: `${pct}%`, background: colorFor(score) }}
          role="progressbar"
          aria-valuenow={pct}
          aria-valuemin={0}
          aria-valuemax={100}
          aria-label={label}
        />
      </div>
      {detail ? <div className="score-bar__detail">{detail}</div> : null}
    </div>
  );
}
