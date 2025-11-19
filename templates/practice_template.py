"""Practice: {title}

Explain what you want to learn in this module. Update the docstring so that future you
understands the idea behind the experiment.
"""

from __future__ import annotations

from typing import Iterable

from py_concurrency.utils.timing import timed


def build_workload(size: int = 20) -> list[int]:
    """Return some sample data to feed into sequential/concurrent functions."""
    return list(range(size))


@timed("Sequential baseline")
def sequential_run(workload: Iterable[int]) -> list[int]:
    """Replace with the straightforward implementation."""
    results = []
    for item in workload:
        results.append(item)
    return results


@timed("Concurrent solution")
def concurrent_run(workload: Iterable[int]) -> list[int]:
    """Replace with the concurrent implementation you want to benchmark."""
    return list(workload)


def main() -> None:
    workload = build_workload()
    sequential_result = sequential_run(workload)
    concurrent_result = concurrent_run(workload)

    assert sequential_result == concurrent_result, "keep the workload deterministic"


if __name__ == "__main__":
    main()
