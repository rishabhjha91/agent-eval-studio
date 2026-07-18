import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { ComparePanel } from "../components/ComparePanel";
import { SAMPLE_COMPARISON } from "../sample";

describe("ComparePanel", () => {
  it("shows the overall verdict", () => {
    render(<ComparePanel result={SAMPLE_COMPARISON} />);
    expect(screen.getByTestId("verdict")).toHaveTextContent("Model A wins");
  });

  it("renders both model cards with overall scores", () => {
    render(<ComparePanel result={SAMPLE_COMPARISON} />);
    expect(screen.getByTestId("eval-card-agent-good")).toBeInTheDocument();
    expect(screen.getByTestId("eval-card-agent-bad")).toBeInTheDocument();
  });

  it("flags out-of-scope files and hallucinated imports on the bad run", () => {
    render(<ComparePanel result={SAMPLE_COMPARISON} />);
    expect(screen.getByTestId("out-of-scope")).toHaveTextContent(
      "src/billing/invoice.py",
    );
    expect(screen.getByTestId("hallucinated")).toHaveTextContent("moneyfmt");
  });

  it("marks the winning card", () => {
    render(<ComparePanel result={SAMPLE_COMPARISON} />);
    expect(screen.getByTestId("eval-card-agent-good").className).toContain(
      "eval-card--winner",
    );
  });
});
