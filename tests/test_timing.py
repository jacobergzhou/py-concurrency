from __future__ import annotations

from py_concurrency.utils.timing import timed


def test_timed_preserves_return_value(capsys) -> None:
    @timed("demo")
    def add(a: int, b: int) -> int:
        return a + b

    assert add(1, 2) == 3
    message = capsys.readouterr().out
    assert "demo" in message
    assert "finished" in message


def test_timed_uses_function_name_when_label_missing(capsys) -> None:
    @timed(None)
    def multiply(a: int, b: int) -> int:
        return a * b

    multiply(2, 3)
    message = capsys.readouterr().out
    assert "multiply" in message
