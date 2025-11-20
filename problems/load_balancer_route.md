# Load Balancer Routing

Implement a thread-safe load balancer that assigns requests to backend servers.

## Problem
Create a `LoadBalancer` class responsible for N backend servers. Each server `i` keeps track of:
- `capacity` — maximum number of concurrent requests it can handle.
- `current_load` — number of in-flight requests.

### Methods
- `route_request(request_id) -> server_id | None`
  - Selects the server with the minimal `current_load` among those where `current_load < capacity`.
  - Returns the index/ID of the chosen server, or `None` if all servers are full.
- `finish_request(server_id)`
  - Decrements `current_load` for the specified server when a request finishes.

## Requirements
- Thread-safe for concurrent `route_request` and `finish_request` calls.
- Use a lock (or fine-grained locking) to protect shared state.
- Avoid race conditions that could oversubscribe a server or drop a decrement.

## Extensions (optional)
- Support weighted servers so faster machines receive more traffic.

Use `src/py_concurrency/practice/load_balancer_route.py` to prototype and test the implementation.
