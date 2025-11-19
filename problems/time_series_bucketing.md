# Time-series Bucketing

You receive a list of tuples `(timestamp_iso_str, value)` where the timestamp is formatted like
`"2025-11-18T09:33:00"` (ISO 8601 without timezone). Implement logic that groups entries into
one-minute buckets.

## Requirements
- Return a list of `(minute_start_iso_str, sum)` pairs sorted by ascending minute.
- Each minute bucket covers the half-open interval `[minute_start, minute_start + 1 minute)`.
- Input timestamps are arbitrary (can have gaps, multiple entries per minute, or arrive unsorted).
- Use only the Python standard library (e.g., `datetime`, `collections`).

Build the solution in `src/py_concurrency/practice/time_series_bucketing.py`. Keep this file as the
reference statement while iterating on implementations and experiments.
