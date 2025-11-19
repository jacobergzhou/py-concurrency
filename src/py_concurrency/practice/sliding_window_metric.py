"""Practice: Sliding Window Metric

Problem statement: problems/sliding_window_metric.md

Goal: design an `EventWindow` that maintains the sum of events that landed within the last `K`
seconds while supporting efficient expiration of stale events. The helpers below give you a naive
reference implementation plus a generated workload so you can iterate quickly.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Literal
from collections import deque
from py_concurrency.utils.timing import timed

WINDOW_SIZE = 4


@dataclass(frozen=True)
class Operation:
    """Represents either an add event or a sum query."""

    kind: Literal["add", "sum"]
    timestamp: int
    amount: int | None = None  # present only for add operations


class EventWindow:
    """Replace this stub with an efficient sliding window structure."""

    def __init__(self) -> None:
        self._placeholder: list[tuple[int, int]] = []
        self.queue = deque()
        self.window_sum = 0

    def add(self, t: int, x: int) -> None:
        """Record an event."""
        self.queue.append((t,x))
        self.window_sum += x
        while self.queue and self.queue[0][0] <= t - WINDOW_SIZE:
            old = self.queue.popleft()
            self.window_sum -= old[1]
        

    def sum_last_k_seconds(self, t: int) -> int:
        """Return the sum of all x with timestamps in [t-K+1, t]."""
        while self.queue and self.queue[0][0] <= t - WINDOW_SIZE:
            old = self.queue.popleft()
            self.window_sum -= old[1]
        return self.window_sum


class NaiveEventWindow:
    """Straightforward solution that re-scans the full history each time."""

    def __init__(self) -> None:
        self._events: list[tuple[int, int]] = []

    def add(self, t: int, x: int) -> None:
        self._events.append((t, x))

    def sum_last_k_seconds(self, t: int) -> int:
        start = t - WINDOW_SIZE + 1
        return sum(value for event_t, value in self._events if start <= event_t <= t)


def build_workload() -> list[Operation]:
    """Scripted stream you can tweak to stress-test the data structure."""
    return [
        Operation("add", 1, 5),
        Operation("add", 2, 7),
        Operation("sum", 2),  # expects 12
        Operation("add", 5, 3),
        Operation("sum", 5),  # expects 10 (events at t=2 and t=5)
        Operation("add", 6, 4),
        Operation("add", 7, 10),
        Operation("sum", 7),  # expects 17 (events at t=5,6,7)
        Operation("sum", 9),  # expects 14 (events at t=6,7)
        Operation("add", 12, 8),
        Operation("sum", 12),  # expects 8
    ]


def _run_stream(window: NaiveEventWindow | EventWindow, workload: Iterable[Operation]) -> list[int]:
    results: list[int] = []
    for op in workload:
        if op.kind == "add":
            assert op.amount is not None
            window.add(op.timestamp, op.amount)
        else:
            results.append(window.sum_last_k_seconds(op.timestamp))
    return results


@timed("Reference (naive)")
def sequential_run(workload: Iterable[Operation]) -> list[int]:
    reference = NaiveEventWindow()
    return _run_stream(reference, workload)


@timed("Candidate implementation")
def concurrent_run(workload: Iterable[Operation]) -> list[int]:
    window = EventWindow()
    return _run_stream(window, workload)


def main() -> None:
    workload = build_workload()
    sequential_result = sequential_run(workload)
    concurrent_result = concurrent_run(workload)

    assert sequential_result == concurrent_result


if __name__ == "__main__":
    main()
