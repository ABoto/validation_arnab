"""
rules/built_in.py — Concrete validation rules and rule factory.

─────────────────────────────────────────────────────────
DAY 1 TASK
─────────────────────────────────────────────────────────
Implement concrete rules as subclasses of BaseValidator.
Each mirrors a function in starter/validate_trips.py:

  NullCheckRule(field: str)
    — Fails when the field is absent, None, or an empty/whitespace string.
    — Mirror of: check_not_null()

  RangeRule(field: str, min: float, max: float)
    — Fails when the field is not a number or is outside [min, max].
    — Mirror of: check_range()

  CoordinateRule(field: str, min: float, max: float)
    — Fails when a geographic coordinate is outside the bounding box.
    — Mirror of: check_coordinate()
    — Hint: the logic is almost identical to RangeRule — what does this
      tell you about inheritance or composition?

Part B (stretch):
  DateFormatRule(field: str, fmt: str = "%Y-%m-%d %H:%M:%S")
    — Fails when the field cannot be parsed as a datetime in the given format.
    — Mirror of: check_date_format()

Each rule must store self.field and any other config params in __init__.
The 'type' name used in config/rules.yaml is the snake_case class name:
  NullCheckRule  → null_check_rule
  RangeRule      → range_rule
  CoordinateRule → coordinate_rule
  DateFormatRule → date_format_rule
"""
#### Task 1 implementation ####

from validify.core.base import BaseValidator


class NullCheckRule(BaseValidator):
    def __init__(self, field: str):
        self.field = field

    def validate(self, record: dict) -> bool:
        value = record.get(self.field, "")
        return value not in (None, "", " ")

    @property
    def message(self) -> str:
        return f"{self.field} must not be null"


class RangeRule(BaseValidator):

    def __init__(self, field: str, min_value: float, max_value: float):
        self.field = field
        self.min = min_value
        self.max = max_value

    def validate(self, record: dict) -> bool:
        try:
            value = float(record[self.field])
        except (KeyError, ValueError, TypeError):
            return False
        return self.min <= value <= self.max

    @property
    def message(self) -> str:
        return f"{self.field} must be between {self.min} and {self.max}"


class CoordinateRule(BaseValidator):

    def __init__(self, field: str, min_value: float, max_value: float):
        self.field = field
        self.min = min_value
        self.max = max_value

    def validate(self, record: dict) -> bool:
        try:
            coord = float(record[self.field])
        except (KeyError, ValueError, TypeError):
            return False
        return self.min <= coord <= self.max

    @property
    def message(self) -> str:
        return f"{self.field} is outside valid coordinate range ({self.min}, {self.max})"

class AllowedValuesRule(BaseValidator):
    def __init__(self, field: str, allowed: list[str]):
        self.field = field
        self.allowed = allowed
        self._message = ""  
    
    def validate(self, record: dict) -> bool:
        value = str(record.get(self.field, "")).strip()
        if value not in self.allowed:
            self._message = (
                f"{self.field}: '{value}' is not one of {self.allowed}"
            )
            return False
        return True

    @property
    def message(self) -> str:
        return self._message
"""
─────────────────────────────────────────────────────────
DAY 3 TASK — add RegexRule and RuleFactory
─────────────────────────────────────────────────────────
  RegexRule(field: str, pattern: str)
    — Fails when the field value does not match re.fullmatch(pattern, value).
    — Mirror of: check_allowed_values() but more general.
    — Needed for the payment_type rule in config/rules.yaml.
    — type name: regex_rule

  RuleFactory:
      @staticmethod
      def from_config(path: str) -> list[BaseValidator]:
          # 1. Open and parse the YAML file.
          # 2. For each entry, look up the class: ValidatorRegistry.get(entry["type"])
          # 3. Instantiate it passing the remaining keys as kwargs.
          # 4. Return the list.

─────────────────────────────────────────────────────────
DAY 5 — Git exercise
─────────────────────────────────────────────────────────
On a feature branch, add RegexRule if not done yet, confirm it is
registered and works via a unit test, then merge back to main.
"""

# import re  # noqa: F401 — needed by RegexRule
# import yaml  # noqa: F401 — needed by RuleFactory

# from validify.core.base import BaseValidator  # noqa: F401
# from validify.core.exceptions import ConfigError  # noqa: F401
# from validify.rules.registry import ValidatorRegistry  # noqa: F401


# ---------------------------------------------------------------------------
# YOUR CODE BELOW
# ---------------------------------------------------------------------------
