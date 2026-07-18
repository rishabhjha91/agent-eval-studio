import type { CompareResult } from "./types";

const BASE_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

export async function fetchSampleComparison(
  signal?: AbortSignal,
): Promise<CompareResult> {
  const res = await fetch(`${BASE_URL}/sample`, { signal });
  if (!res.ok) {
    throw new Error(`API error ${res.status}`);
  }
  return (await res.json()) as CompareResult;
}
