"""
utils/decorators.py — Reusable function decorators.

─────────────────────────────────────────────────────────
DAY 2 TASK — Part A (mandatory)
─────────────────────────────────────────────────────────
Implement @timeit:
  - Measures wall-clock time from before to after the function call.
  - Prints: [timeit] <function_name> took 0.042s
  - Must preserve the original function's __name__ and __doc__ (use functools.wraps).
  - Works on synchronous functions first.

Usage:
    @timeit
    def run_validation(records, rules):
        ...

""" 

"""
─────────────────────────────────────────────────────────
DAY 2 TASK — Part B (stretch)
─────────────────────────────────────────────────────────
Implement @log_call:
  - Prints: [log_call] calling <function_name>(<arg1>, kwarg=<value>)
  - Must use functools.wraps.
  - Useful for tracing which rules run on which records during debugging.

Usage:
    @log_call
    def validate(self, record):
        ...

─────────────────────────────────────────────────────────
HINTS
─────────────────────────────────────────────────────────
  - Use functools.wraps to preserve the original function's metadata.
  - Use time.perf_counter() (not time.time()) for accurate elapsed time.
  - A decorator is just a function that takes a function and returns a function.
"""

from functools import wraps  # noqa: F401
import time  # noqa: F401
from typing import Any, Callable, TypeVar  # noqa: F401

F = TypeVar("F", bound=Callable[..., Any])


def timeit(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = fn(*args, **kwargs)
        end = time.perf_counter()
        duration = end - start
        print(f"[timeit] {fn.__name__} took {duration:.4f}s")
        return result

    return wrapper


def log_call(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        print(f"[log_call] Calling: {fn.__name__}")
        print(f"  args: {args}")
        print(f"  kwargs: {kwargs}")
        result = fn(*args, **kwargs)
        print(f"[log_call] {fn.__name__} returned: {result}")
        return result

    return wrapper


# ---------------------------------------------------------------------------
# YOUR CODE BELOW
# ---------------------------------------------------------------------------
