"""
engine/runner.py — Validation execution engines.

─────────────────────────────────────────────────────────
DAY 4 TASK — Part A (mandatory)
─────────────────────────────────────────────────────────
Implement two execution functions and benchmark them.

1. run_sequential(records, rules) -> list[ValidationResult]
   — Plain for-loop over records, calling each rule on each record.
   — This is the baseline. Apply @timeit to measure it.

2. run_threaded(records, rules, workers=4) -> list[ValidationResult]
   — Use ThreadPoolExecutor(max_workers=workers).
   — Each submitted task validates one record against all rules.
   — Protect the shared results list with a threading.Lock().
   — Apply @timeit and compare the elapsed time with run_sequential.

After both are working, add a comment at the top of this file:
    # sequential: X.XXs   threaded(4): X.XXs   (measured on taxi_trips_sample.csv)

─────────────────────────────────────────────────────────
DISCUSSION QUESTION (think about this while you implement)
─────────────────────────────────────────────────────────
Why does threading not always make CPU-bound work faster in Python?
What would change if you used ProcessPoolExecutor instead?

─────────────────────────────────────────────────────────
DAY 4 TASK — Part B (stretch)
─────────────────────────────────────────────────────────
3. async def run_async(records, rules) -> list[ValidationResult]
   — Use asyncio.gather with a list of coroutines.
   — Each coroutine validates one record against all rules.
   — Return the flattened list of ValidationResult objects.
"""

import asyncio  # noqa: F401
from concurrent.futures import ThreadPoolExecutor  # noqa: F401
from threading import Lock  # noqa: F401

from validify.core.base import BaseValidator  # noqa: F401
from validify.core.models import ValidationResult  # noqa: F401

# Apply your @timeit decorator here once you have implemented it in utils/decorators.py


# ---------------------------------------------------------------------------
# YOUR CODE BELOW
# ---------------------------------------------------------------------------

from typing import Iterable, List
from validify.utils.decorators import timeit


@timeit
def run_sequential(records: Iterable[dict], rules: Iterable[BaseValidator]) -> List[ValidationResult]:
    """
    Runs validations in a simple sequential loop.
    This is the baseline implementation (Day 4 requirement).
    """
    results: List[ValidationResult] = []

    for record in records:
        for rule in rules:
            results.append(rule(record))

    return results


@timeit
def run_threaded(records: Iterable[dict], rules: Iterable[BaseValidator], workers: int = 4) -> List[ValidationResult]:
    """
    Runs validations in parallel using ThreadPoolExecutor.
    Each record is validated in a separate worker thread.
    """

    results: List[ValidationResult] = []
    lock = Lock()   # ensures thread-safe writes to shared list

    def process_record(record: dict):
        row_results = [rule(record) for rule in rules]
        with lock:
            results.extend(row_results)

    with ThreadPoolExecutor(max_workers=workers) as executor:
        for record in records:
            executor.submit(process_record, record)

    return results


# -------------------------------------------------------------------------
# Stretch Goal (Optional): ASYNC Runner
# -------------------------------------------------------------------------

async def run_async(records: Iterable[dict], rules: Iterable[BaseValidator]) -> List[ValidationResult]:
    """
    OPTIONAL (Day‑4 Stretch): Run validations using asyncio.gather.
    Note: This only helps if rules are I/O-bound.
    """

    async def validate_row(record):
        return [rule(record) for rule in rules]

    tasks = [asyncio.create_task(validate_row(record)) for record in records]

    grouped_results = await asyncio.gather(*tasks)

    # flatten list[list[ValidationResult]] → list[ValidationResult]
    results = [item for group in grouped_results for item in group]
    return results