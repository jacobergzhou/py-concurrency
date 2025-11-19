"""Small utilities to measure sequential vs. concurrent workloads."""

from __future__ import annotations

import functools
import time
from typing import Any, Callable, TypeVar

R = TypeVar("R")


def _format_duration(seconds: float) -> str:
    if seconds >= 1:
        return f"{seconds:0.3f}s"
    return f"{seconds * 1_000:0.2f}ms"


def timed(label: str | None = None) -> Callable[[Callable[..., R]], Callable[..., R]]:
    """Decorator that prints how long the wrapped function took to execute."""

    def decorator(func: Callable[..., R]) -> Callable[..., R]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> R:
            start = time.perf_counter()
            result = func(*args, **kwargs)
            duration = time.perf_counter() - start
            text = label or func.__name__
            print(f"[{text}] finished in {_format_duration(duration)}")
            return result

        return wrapper

    return decorator


__all__ = ["timed"]
