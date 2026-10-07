"""LLM explanation client with streaming performance metrics.

Uses an OpenAI-compatible /v1/chat/completions endpoint and only Python's
standard library. API credentials are read from environment variables.
"""
from dataclasses import dataclass, asdict
import json
import os
import time
from urllib import request


@dataclass
class LLMMetrics:
    success: bool
    ttft_ms: float | None
    total_latency_ms: float
    output_tokens: int
    tokens_per_second: float
    error: str | None = None

    def to_dict(self):
        return asdict(self)


class LLMAnalyzer:
    def __init__(self, api_key=None, base_url=None, model=None, timeout=30):
        self.api_key = api_key or os.getenv("LLM_API_KEY")
        self.base_url = (base_url or os.getenv("LLM_BASE_URL", "https://api.openai.com/v1")).rstrip("/")
        self.model = model or os.getenv("LLM_MODEL", "gpt-4o-mini")
        self.timeout = timeout

    @staticmethod
    def build_prompt(results):
        payload = json.dumps(results, sort_keys=True, default=str)
        return (
            "You are explaining optimization and ML experiment results. "
            "Use only the supplied JSON. Do not invent causes or values. "
            "Summarize the best/rest findings, important rules or model results, "
            "and statistical comparisons in concise plain English. "
            "If evidence is missing, say that it is unavailable.\n\nRESULTS:\n" + payload
        )

    def analyze(self, results):
        if not self.api_key:
            raise ValueError("LLM_API_KEY is required")

        body = json.dumps({
            "model": self.model,
            "stream": True,
            "stream_options": {"include_usage": True},
            "messages": [{"role": "user", "content": self.build_prompt(results)}],
        }).encode("utf-8")
        req = request.Request(
            self.base_url + "/chat/completions",
            data=body,
            headers={"Authorization": "Bearer " + self.api_key, "Content-Type": "application/json"},
            method="POST",
        )

        started = time.perf_counter()
        first_token_at = None
        pieces = []
        output_tokens = 0
        try:
            with request.urlopen(req, timeout=self.timeout) as response:
                for raw in response:
                    line = raw.decode("utf-8").strip()
                    if not line.startswith("data:"):
                        continue
                    data = line[5:].strip()
                    if data == "[DONE]":
                        break
                    event = json.loads(data)
                    choices = event.get("choices", [])
                    if choices:
                        content = choices[0].get("delta", {}).get("content")
                        if content:
                            if first_token_at is None:
                                first_token_at = time.perf_counter()
                            pieces.append(content)
                    usage = event.get("usage")
                    if usage:
                        output_tokens = usage.get("completion_tokens", output_tokens)

            ended = time.perf_counter()
            latency = ended - started
            ttft = None if first_token_at is None else (first_token_at - started) * 1000
            rate = output_tokens / latency if latency > 0 else 0.0
            return "".join(pieces), LLMMetrics(
                success=True,
                ttft_ms=ttft,
                total_latency_ms=latency * 1000,
                output_tokens=output_tokens,
                tokens_per_second=rate,
            )
        except Exception as exc:
            ended = time.perf_counter()
            return "", LLMMetrics(
                success=False,
                ttft_ms=None,
                total_latency_ms=(ended - started) * 1000,
                output_tokens=0,
                tokens_per_second=0.0,
                error=str(exc),
            )
