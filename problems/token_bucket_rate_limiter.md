# Token-Bucket Rate Limiter

Implement a thread-safe rate limiter using the token bucket algorithm.

## Problem
Create a class with the following interface:

- `__init__(rate: float, capacity: int)`
  - `rate`: tokens refilled per second (e.g., 5 QPS).
  - `capacity`: maximum number of tokens the bucket can hold.
- `allow() -> bool`
  - Refill tokens based on elapsed time since the previous call.
  - If at least one token is available, consume it and return `True`.
  - Otherwise return `False` (no blocking).

## Requirements
- Safe under concurrent `allow()` calls from multiple threads.
- Use `time.monotonic()` for elapsed time calculations and `threading.Lock` for synchronization.
- Keep the logic reusable for use cases like per-model or per-tenant inference QPS limits.

Build experiments in `src/py_concurrency/practice/token_bucket_rate_limiter.py` to validate the
implementation (e.g., spawn worker threads that call `allow()` and record when requests are allowed
or dropped).
