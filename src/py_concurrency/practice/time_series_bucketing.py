"""Practice: Time Series Bucketing

Problem statement: problems/time_series_bucketing.md

Goal: ingest arbitrary `(timestamp_iso_str, value)` pairs and collapse them into one-minute buckets.
Use this scaffold to implement different strategies (sorting, streaming, grouping) while comparing
against a straightforward reference implementation.
"""

from __future__ import annotations

from collections import defaultdict
from datetime import datetime
from typing import Iterable, List, Tuple
from datetime import datetime

from py_concurrency.utils.timing import timed

Event = Tuple[str, int]
Bucket = Tuple[str, int]


def bucket_events(events: Iterable[Event]) -> List[Bucket]:
    """Replace this implementation with your own approach."""
    d = {}
    for time, val in events:
        minute = time[:16] + ":00"
        if minute not in d:
            d[minute] = 0
        d[minute] += val
    ls = []
    for k,v in d.items():
        ls.append((k,v))
    ls.sort(key = lambda x: x[0])
    return ls

def reference_bucket_events(events: Iterable[Event]) -> List[Bucket]:
    """Simple baseline that sorts every event then groups by minute."""

    def minute_key(timestamp: str) -> datetime:
        dt = datetime.fromisoformat(timestamp)
        return dt.replace(second=0, microsecond=0)

    totals: defaultdict[datetime, int] = defaultdict(int)
    for ts, value in sorted(events, key=lambda item: item[0]):
        totals[minute_key(ts)] += value

    return [(minute.isoformat(), totals[minute]) for minute in sorted(totals)]


def build_workload() -> list[Event]:
    """Sample data covering multiple minutes, duplicates, and out-of-order entries."""
    return [
        ("2025-11-18T09:33:00", 5),
        ("2025-11-18T09:33:42", 7),
        ("2025-11-18T09:35:00", 2),
        ("2025-11-18T09:33:15", 4),
        ("2025-11-18T09:36:59", 6),
        ("2025-11-18T09:36:05", 3),
        ("2025-11-18T09:38:00", 10),
        ("2025-11-18T09:34:12", 11),
    ]


@timed("Reference implementation")
def sequential_run(workload: Iterable[Event]) -> List[Bucket]:
    return reference_bucket_events(workload)


@timed("Candidate implementation")
def concurrent_run(workload: Iterable[Event]) -> List[Bucket]:
    return bucket_events(workload)


def main() -> None:
    workload = build_workload()
    sequential_result = sequential_run(workload)
    candidate_result = concurrent_run(workload)

    print("Reference buckets:", sequential_result)
    print("Candidate buckets:", candidate_result)
    assert sequential_result == candidate_result


if __name__ == "__main__":
    main()
