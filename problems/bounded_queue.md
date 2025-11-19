# Bounded Blocking Queue

Practice building a producer–consumer queue with backpressure.

## Problem
Implement a `BoundedBlockingQueue` class with the following API:

- `__init__(capacity: int)`
- `put(item)` — block if the queue is full until space becomes available.
- `get()` — block if the queue is empty until an item becomes available.
- `size()` — return the current number of queued items (non-blocking).

### Requirements
- Use `threading.Condition` plus an internal list/deque for storage.
- No busy-waiting (avoid `while True: pass` or repeated sleep loops).
- Coordinate producers and consumers fairly so that blocked threads are awakened when state changes.

## Experiment harness
Create a script (`src/py_concurrency/practice/bounded_queue.py`) that spawns multiple producer
threads and multiple consumer threads. Each producer should push a sequence of items, and each
consumer should pop and process them. Log events such as `"producer-1 put 42"` or
`"consumer-2 got 42"` to observe the interleaving and ensure the queue enforces capacity limits.
