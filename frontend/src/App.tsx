import { useState } from "react";
import { fetchSampleComparison } from "./api";
import { ComparePanel } from "./components/ComparePanel";
import { SAMPLE_COMPARISON } from "./sample";
import type { CompareResult } from "./types";

export default function App() {
  const [result, setResult] = useState<CompareResult>(SAMPLE_COMPARISON);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function loadFromApi() {
    setLoading(true);
    setError(null);
    try {
      const live = await fetchSampleComparison();
      setResult(live);
    } catch {
      setError("Could not reach the API. Showing bundled sample data.");
      setResult(SAMPLE_COMPARISON);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="app">
      <header className="app__header">
        <h1>AgentEval Studio</h1>
        <p>Coding-agent trajectory evaluation: correctness, scope, grounding, efficiency.</p>
        <button onClick={loadFromApi} disabled={loading}>
          {loading ? "Loading..." : "Load from API"}
        </button>
        {error && (
          <p className="app__error" role="alert">
            {error}
          </p>
        )}
      </header>

      <h2>
        Task: <code>{result.report_a.task_id}</code>
      </h2>
      <ComparePanel result={result} />
    </main>
  );
}
