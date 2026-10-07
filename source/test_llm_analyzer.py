import io
import json
import LLMAnalyzer as module
from LLMAnalyzer import LLMAnalyzer


class FakeResponse:
    def __init__(self, lines):
        self.lines = lines

    def __enter__(self):
        return iter(self.lines)

    def __exit__(self, exc_type, exc, tb):
        return False


def sse(payload):
    return ("data: " + json.dumps(payload) + "\n").encode()


def test_prompt_is_grounded_in_supplied_results():
    prompt = LLMAnalyzer.build_prompt({"best": 4, "rest": 16})
    assert '"best": 4' in prompt
    assert '"rest": 16' in prompt
    assert "Do not invent" in prompt


def test_missing_api_key(monkeypatch):
    monkeypatch.delenv("LLM_API_KEY", raising=False)
    analyzer = LLMAnalyzer(api_key=None)
    try:
        analyzer.analyze({"best": []})
        assert False, "expected ValueError"
    except ValueError as exc:
        assert "LLM_API_KEY" in str(exc)


def test_streaming_response_and_metrics(monkeypatch):
    lines = [
        sse({"choices": [{"delta": {"content": "Best rows "}}]}),
        sse({"choices": [{"delta": {"content": "have lower cost."}}]}),
        sse({"choices": [], "usage": {"completion_tokens": 6}}),
        b"data: [DONE]\n",
    ]
    monkeypatch.setattr(module.request, "urlopen", lambda req, timeout: FakeResponse(lines))
    analyzer = LLMAnalyzer(api_key="test-key")
    text, metrics = analyzer.analyze({"best": {"cost": 1}, "rest": {"cost": 5}})

    assert text == "Best rows have lower cost."
    assert metrics.success is True
    assert metrics.ttft_ms is not None
    assert metrics.total_latency_ms >= metrics.ttft_ms
    assert metrics.output_tokens == 6
    assert metrics.tokens_per_second >= 0


def test_provider_failure_is_measured(monkeypatch):
    def fail(req, timeout):
        raise RuntimeError("provider unavailable")

    monkeypatch.setattr(module.request, "urlopen", fail)
    text, metrics = LLMAnalyzer(api_key="test-key").analyze({"result": "x"})
    assert text == ""
    assert metrics.success is False
    assert "provider unavailable" in metrics.error
    assert metrics.total_latency_ms >= 0
