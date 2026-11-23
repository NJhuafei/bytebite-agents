"""Pydantic v2 data contracts for ByteBite."""

from typing import Literal

from pydantic import BaseModel, Field, field_validator


class FoodItem(BaseModel):
    """Canonical representation of a single dish extracted from user input."""

    name: str = Field(min_length=2, description="Canonical dish name")
    est_kcal: int = Field(gt=0, le=2500, description="Estimated kilocalories")
    cook_method: Literal["steamed", "boiled", "stir_fried", "deep_fried"]
    allergens: list[str] = Field(
        default_factory=list,
        description="Explicit allergen tags (e.g., peanut, dairy, shellfish, soy, gluten)",
    )

    @field_validator("allergens")
    @classmethod
    def normalize_tags(cls, v: list[str]) -> list[str]:
        """Normalize allergen strings to deduplicated lowercase tags."""
        return sorted({tag.strip().lower() for tag in v if tag.strip()})
