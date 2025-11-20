# Request Batcher

Implement a class that batches requests and processes them in the background.

## API
```
batcher = RequestBatcher(max_batch_size: int)
result = batcher.submit(request)
```

- `submit(request) -> result`
  - Called by multiple threads.
  - Adds the request to a shared pending list.
  - Blocks until a background worker processes a batch containing this request.
  - Returns the per-request result.

## Background worker
- Runs in its own thread.
- Waits until there is at least one pending request.
- Takes up to `max_batch_size` pending requests per batch.
- Processes them via `process_batch(requests) -> results`.
- Writes each result back to the corresponding pending item and wakes the waiting `submit()` callers.

For this exercise, `process_batch` can implement:
- If the request is a string, convert it to uppercase.
- If the request is a number, add 1.

## Requirements
- Use `threading.Thread` plus `threading.Lock` and/or `threading.Condition` for coordination.
- Store pending items in a Python list.
- No busy-waiting loops.
- No lost or double-processed requests; each `submit()` must return the correct result.

Use `src/py_concurrency/practice/request_batcher.py` as the playground to build and test the batching
logic.
