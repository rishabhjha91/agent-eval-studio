from fastapi.testclient import TestClient

from ageval import samples
from ageval.api import app

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_sample_endpoint():
    r = client.get("/sample")
    assert r.status_code == 200
    assert r.json()["winner"] == "a"


def test_evaluate_endpoint():
    payload = {
        "task": samples.SAMPLE_TASK.model_dump(),
        "trajectory": samples.GOOD_TRAJECTORY.model_dump(),
    }
    r = client.post("/evaluate", json=payload)
    assert r.status_code == 200
    body = r.json()
    assert body["test_pass_rate"] == 1.0
    assert body["overall_score"] > 0.9


def test_evaluate_html_endpoint():
    payload = {
        "task": samples.SAMPLE_TASK.model_dump(),
        "trajectory": samples.BAD_TRAJECTORY.model_dump(),
    }
    r = client.post("/evaluate/html", json=payload)
    assert r.status_code == 200
    assert "text/html" in r.headers["content-type"]
    assert "AgentEval Studio" in r.text


def test_compare_endpoint():
    payload = {
        "task": samples.SAMPLE_TASK.model_dump(),
        "trajectory_a": samples.GOOD_TRAJECTORY.model_dump(),
        "trajectory_b": samples.BAD_TRAJECTORY.model_dump(),
    }
    r = client.post("/compare", json=payload)
    assert r.status_code == 200
    assert r.json()["winner"] == "a"
