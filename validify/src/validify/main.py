"""
src/validify/main.py — CLI entry point for the validation pipeline.

─────────────────────────────────────────────────────────
DAY 1 TASK (create this file)
─────────────────────────────────────────────────────────
Create a runner that produces the same output as starter/validate_trips.py
but uses the new class hierarchy:

  1. Accept a CSV path from sys.argv[1].
  2. Open the CSV with open() + csv.DictReader (plain, no context manager yet).
  3. Instantiate rules manually:
       rules = [NullCheckRule("vendor_id"), RangeRule("passenger_count", 1, 8), ...]
  4. For each record, call each rule: result = rule(record)  # __call__
  5. Collect ValidationResult objects.
  6. Print a summary (same format as the starter script).
"""
#### Task 1 implementatoin ####
# import csv
# import sys
# import time
# from pathlib import Path

# from validify.utils.decorators import timeit, log_call
# from validify.rules.built_in import (
#     NullCheckRule,
#     RangeRule,
#     AllowedValuesRule,
# )


# def load_records(csv_path: Path):
#     with open(csv_path, encoding="utf-8", newline="") as fh:
#         reader = csv.DictReader(fh)
#         for row in reader:
#             yield row


# @timeit
# def slow_function():
#     time.sleep(0.5)
#     return "done"


# @timeit
# @log_call
# def main():
#     if len(sys.argv) < 2:
#         print("Usage: python -m validify.main data/taxi_trips_sample.csv")
#         sys.exit(1)

#     csv_path = Path(sys.argv[1])
#     if not csv_path.exists():
#         print(f"Error: file not found — {csv_path}")
#         sys.exit(1)

#     # -----------------------
#     # Instantiate RULES (Day 1 only)
#     # -----------------------
#     rules = [
#         NullCheckRule("vendor_id"),
#         NullCheckRule("pickup_datetime"),
#         NullCheckRule("dropoff_datetime"),
#         RangeRule("passenger_count", 1, 8),
#         RangeRule("trip_distance", 0.1, 200.0),
#         RangeRule("fare_amount", 0.01, 500.0),
#         RangeRule("total_amount", 0.01, 600.0),
#         AllowedValuesRule("payment_type", ["Cash", "Card"]),
#         # Stretch rule
#         AllowedValuesRule(
#             "payment_type",
#             ["Credit", "Cash", "No Charge", "Dispute"],
#         ),
#     ]

#     total = 0
#     passed = 0
#     failed = 0

#     for record in load_records(csv_path):
#         total += 1

#         results = [rule(record) for rule in rules]
#         failures = [r for r in results if not r.passed]

#         if failures:
#             failed += 1
#         else:
#             passed += 1

#     # -----------------------
#     # Print summary (Day 1)
#     # -----------------------
#     print("\n============================================================")
#     print("VALIDATION REPORT")
#     print("============================================================")
#     print(f"  Total records : {total}")
#     print(f"  Passed        : {passed}")
#     print(f"  Failed        : {failed}")
#     print(f"  Pass rate     : {passed / total * 100:.1f}%")
#     print("============================================================")


# ###### Checking day 2 task, registry creation ###########

# from validify.rules.built_in import NullCheckRule  # import triggers registration
# from validify.rules.registry import ValidatorRegistry

# assert ValidatorRegistry.get("null_check_rule") is NullCheckRule
# print("Registry works!")
# print(ValidatorRegistry._registry)



# if __name__ == "__main__":
#     main()




"""
─────────────────────────────────────────────────────────
DAY 2 TASK (update this file)
─────────────────────────────────────────────────────────
  - Apply @timeit to the main validation function.
  - Build a Report dataclass from the results and print pass_rate from it.

─────────────────────────────────────────────────────────
DAY 3 TASK (update this file)
─────────────────────────────────────────────────────────
  - Replace the hardcoded rules list with:
      rules = RuleFactory.from_config("config/rules.yaml")
  - Wrap the CSV open() in DatasetLoader context manager (stretch).
  - Run records through normalize_record before validation.

─────────────────────────────────────────────────────────
Run with:
    python src/validify/main.py data/taxi_trips_sample.csv
─────────────────────────────────────────────────────────
"""

import csv
import sys
from pathlib import Path

from validify.rules.built_in import RuleFactory
from validify.transforms.pipeline import pipe, normalize_record
from validify.utils.decorators import timeit
from validify.core.models import Report, ValidationResult
from validify.transforms.pipeline import DatasetLoader, pipe, normalize_record

def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python src/validify/main.py C:/Users/YM316EV/Workspace/TestBoto/Capstone/validation_arnab/validify/data/taxi_trips_sample.csv")
        sys.exit(1)

    csv_path = Path(sys.argv[1])
    if not csv_path.exists():
        print(f"Error: file not found — {csv_path}")
        sys.exit(1)

    # ---------------------------------------------------------------------------
    # YOUR CODE BELOW — follow the Day 1 steps in the docstring above
    # ---------------------------------------------------------------------------

    # ----------------------------- DAY 3 CODE -------------------------------

    rules = RuleFactory.from_config("config/rules.yaml")

    # with open(csv_path, "r", encoding="utf-8") as f:
        # records = list(csv.DictReader(f))



    preprocess = pipe(normalize_record)

    @timeit
    def run_validations():
        results = []
        preprocess = pipe(normalize_record)

        with DatasetLoader(csv_path) as records:   # ✅ generator
            for record in records:
                record = preprocess(record)        # ✅ cleaned record
                for rule in rules:
                    results.append(rule(record))

        return results


    results = run_validations()

    total = len(results)
    passed = sum(r.passed for r in results)
    failed = total - passed

    report = Report(total, passed, failed, results)

    print("\n==================== VALIDATION REPORT (DAY 3) ====================")
    print(f"Total checks : {report.total}")
    print(f"Passed       : {report.passed}")
    print(f"Failed       : {report.failed}")
    print(f"Pass Rate    : {report.pass_rate:.2f}%")
    print("==================================================================\n")

    # ###### Checking day 2 task, registry creation ###########

from validify.rules.built_in import NullCheckRule  # import triggers registration
from validify.rules.registry import ValidatorRegistry

assert ValidatorRegistry.get("null_check_rule") is NullCheckRule
print("Registry works!")
print(ValidatorRegistry._registry)



if __name__ == "__main__":
    main()
