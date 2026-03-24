FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml README.md ./
COPY src ./src
COPY templates ./templates
COPY static ./static
COPY data ./data

RUN pip install --no-cache-dir uv \
    && uv pip install --system .

EXPOSE 8000

CMD ["uvicorn", "voice_agent_app.main:app", "--host", "0.0.0.0", "--port", "8000"]

*** Add File: /Users/arifalam/Documents/New project/voice-agent-showcase/src/voice_agent_app/monitoring.py
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from time import perf_counter


@dataclass
class MetricsRegistry:
    counters: Counter[str] = field(default_factory=Counter)
    latency_samples: list[float] = field(default_factory=list)

    def increment(self, key: str, count: int = 1) -> None:
        self.counters[key] += count

    def observe(self, latency_seconds: float) -> None:
        self.latency_samples.append(latency_seconds)


metrics = MetricsRegistry()


class RequestTimer:
    def __enter__(self) -> "RequestTimer":
        self.started_at = perf_counter()
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        metrics.observe(perf_counter() - self.started_at)

