# Unsafe vs. Safe Counter

Implement two counter classes that illustrate the effect of race conditions under multithreading.

## UnsafeCounter
- Holds an integer value starting at 0.
- `increment()` performs `self.value += 1` with no synchronization.

## SafeCounter
- Same API as `UnsafeCounter`.
- Guard concurrent increments with `threading.Lock` so every call updates the value atomically.

## Experiment harness
Write a script that:
1. Spawns 10 threads.
2. Each thread invokes `increment()` 100_000 times.
3. Prints the final value for both classes, demonstrating that `UnsafeCounter.value != 1_000_000`
   most of the time while `SafeCounter.value == 1_000_000`.

Build the experiment in `src/py_concurrency/practice/unsafe_safe_counter.py`. Keep this file as the
reference description while iterating on implementations.
