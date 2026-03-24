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

