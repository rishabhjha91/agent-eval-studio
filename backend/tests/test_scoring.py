from ageval import samples, scoring
from ageval.report import to_html, to_json


def test_good_trajectory_scores_high():
    rep = scoring.evaluate(samples.SAMPLE_TASK, samples.GOOD_TRAJECTORY)
    assert rep.test_pass_rate == 1.0
    assert rep.out_of_scope_files == []
    assert rep.hallucinated_imports == []
    assert rep.overall_score > 0.9


def test_bad_trajectory_scores_low_and_flags_issues():
    rep = scoring.evaluate(samples.SAMPLE_TASK, samples.BAD_TRAJECTORY)
    assert rep.test_pass_rate < 1.0
    # billing + README are outside src/pricing/ and tests/
    assert "src/billing/invoice.py" in rep.out_of_scope_files
    assert "README.md" in rep.out_of_scope_files
    assert "moneyfmt" in rep.hallucinated_imports
    assert rep.overall_score < rep.overall_score + 1  # sanity
    assert rep.overall_score < 0.7


def test_compare_prefers_good():
    result = scoring.compare(
        samples.SAMPLE_TASK, samples.GOOD_TRAJECTORY, samples.BAD_TRAJECTORY
    )
    assert result.winner == "a"
    assert result.per_criterion_winner["correctness"] == "a"
    assert result.per_criterion_winner["scope_control"] == "a"


def test_scope_detection_respects_allowed_paths():
    oos = scoring.out_of_scope_files(samples.SAMPLE_TASK, samples.GOOD_TRAJECTORY)
    assert oos == []


def test_report_serialisation():
    rep = scoring.evaluate(samples.SAMPLE_TASK, samples.GOOD_TRAJECTORY)
    assert '"overall_score"' in to_json(rep)
    html_out = to_html(rep)
    assert "AgentEval Studio" in html_out
    assert "Overall" in html_out


def test_path_prefix_requires_directory_boundary():
    assert scoring._path_allowed(
        "src/pricing/calculator.py", ["src/pricing"]
    )
    assert not scoring._path_allowed(
        "src/pricingx/evil.py", ["src/pricing"]
    )


def test_path_prefix_accepts_exact_path():
    assert scoring._path_allowed("README.md", ["README.md"])
    assert not scoring._path_allowed("README.md.bak", ["README.md"])


def test_explicit_wildcard_matches_string_prefix():
    assert scoring._path_allowed("src/pricingx/legacy.py", ["src/pricing*"])
