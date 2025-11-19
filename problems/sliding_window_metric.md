# Sliding Window / Streaming Metric

You receive a stream of integer events, each represented as a tuple `(t, x)` where `t` is the
timestamp in seconds and events arrive in strictly increasing `t` order.

Design a class `EventWindow` for a fixed window size `K`. Once `K` is chosen it does not change, so
queries always examine the most recent `K` seconds.

- `add(t: int, x: int)` — record an event.
- `sum_last_k_seconds(t: int) -> int` — return the sum of `x` over events whose timestamps fall in
  the inclusive range `[t - K + 1, t]`.

### Requirements
- Each operation should run in amortized `O(1)` or `O(log n)` time.
- Memory usage should be `O(number of events in the last K seconds)`.

Focus on data structures that make it easy to expire old events while keeping the running sum for
recent timestamps. Use this file as the source of truth for the problem statement while iterating
on the implementation under `src/py_concurrency/practice/sliding_window_metric.py`.
