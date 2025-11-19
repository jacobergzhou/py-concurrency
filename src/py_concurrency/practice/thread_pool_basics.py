"""Warm-up practice that compares sequential processing with a thread pool."""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
import time
from typing import Iterable

from py_concurrency.utils.timing import timed


def build_workload(size: int = 12) -> list[int]:
    return list(range(size))


def slow_double(value: int) -> int:
    time.sleep(0.05)
    return value * 2


@timed("Sequential thread work")
def sequential_run(workload: Iterable[int]) -> list[int]:
    return [slow_double(item) for item in workload]


@timed("ThreadPoolExecutor work")
def concurrent_run(workload: Iterable[int]) -> list[int]:
    with ThreadPoolExecutor(max_workers=4) as executor:
        return list(executor.map(slow_double, workload))


def main() -> None:
    workload = build_workload()
    sequential_result = sequential_run(workload)
    concurrent_result = concurrent_run(workload)
    assert sequential_result == concurrent_result


if __name__ == "__main__":
    main()
