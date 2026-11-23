"""Typed State Bus and custom idempotent reducers for ByteBite."""

import operator
from typing import Annotated, TypedDict

from pydantic import BaseModel

from bytebite.schemas import FoodItem


class MealAnalysis(BaseModel):
    """Structured output emitted by analyzer_node."""

    items: list[FoodItem]
    total_est_kcal: int


def merge_unique_logs(existing: list[str], new: list[str]) -> list[str]:
    """Idempotent reducer: preserves order while preventing duplicate logs on retry."""
    seen = set(existing)
    return existing + [entry for entry in new if entry not in seen]


class ByteBiteState(TypedDict, total=False):
    meal_input: str                                          # Overwrite
    user_goal: str                                           # Overwrite
    user_allergies: list[str]                                # Overwrite (e.g., ['peanut', 'dairy'])
    analysis: MealAnalysis                                   # Overwrite
    risk_alert: str                                          # Overwrite
    final_advice: str                                        # Overwrite
    total_tokens: Annotated[int, operator.add]               # Sum ints across nodes
    audit_logs: Annotated[list[str], merge_unique_logs]      # Idempotent dedup append
    # TODO (HW1): Add the following two fields for the Allergen Hard-Stop short-circuit:
    # blocked: bool                                          # True if halted by allergen gate
    # matched_allergens: list[str]                           # Sorted overlap tags
