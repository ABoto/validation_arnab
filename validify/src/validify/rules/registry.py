"""
rules/registry.py — Auto-registration plugin system for validators.

─────────────────────────────────────────────────────────
DAY 2 TASK
─────────────────────────────────────────────────────────
Implement ValidatorRegistry using Python's __init_subclass__ hook.

Requirements:
  - Class-level dict: _registry: dict[str, type] = {}
  - __init_subclass__ must convert the subclass name to snake_case and store it.
    e.g. "NullCheckRule" → "null_check_rule"
  - Class method: get(name: str) -> type
    — Looks up the registry and returns the class.
    — Raises KeyError with a helpful message if the name is not found.

After implementation, make BaseValidator inherit from ValidatorRegistry:

    class BaseValidator(ValidatorRegistry, ABC):
        ...

Then any class that inherits from BaseValidator will auto-register itself
when its module is imported. No manual wiring needed.

─────────────────────────────────────────────────────────
HINT — converting CamelCase to snake_case:
─────────────────────────────────────────────────────────
    import re
    name = re.sub(r"(?<!^)(?=[A-Z])", "_", cls.__name__).lower()
    # "NullCheckRule" → "null_check_rule"

─────────────────────────────────────────────────────────
CHECKPOINT (paste into a Python REPL to verify your work):
─────────────────────────────────────────────────────────
    from validify.rules.built_in import NullCheckRule   # triggers registration
    from validify.rules.registry import ValidatorRegistry

    assert ValidatorRegistry.get("null_check_rule") is NullCheckRule
    print("Registry works!")
"""

# import re  # noqa: F401 — you will need this for snake_case conversion


# ---------------------------------------------------------------------------
# YOUR CODE BELOW
# ---------------------------------------------------------------------------


# from typing import Dict, Type

# class ValidatorRegistry:
#     _registry: Dict[str, Type] = {}

#     def __init_subclass__(cls, **kwargs):
#         super().__init_subclass__(**kwargs)
#         name = cls.__name__
#         snake = ""

#         for i, ch in enumerate(name):
#             if ch.isupper() and i > 0:
#                 snake += "_" + ch.lower()
#             else:
#                 snake += ch.lower()

#         ValidatorRegistry._registry[snake] = cls

#     @classmethod
#     def get(cls, name: str) -> Type:
#         if name not in cls._registry:
#             raise KeyError(f"Validator '{name}' not found in registry.")
#         return cls._registry[name]

import re
from typing import Dict, Type


class ValidatorRegistry:
    _registry: Dict[str, Type] = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        snake = re.sub(r'(?<!^)(?=[A-Z])', '_', cls.__name__).lower()

        ValidatorRegistry._registry[snake] = cls

    @classmethod
    def get(cls, name: str) -> Type:
        if name not in cls._registry:
            raise KeyError(
                f"Validator '{name}' not found in registry. Available: {list(cls._registry.keys())}"
            )
        return cls._registry[name]