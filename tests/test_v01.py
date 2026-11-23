"""Hermetic offline pytest suite for ByteBite v0.1 (0 network calls)."""

from unittest.mock import MagicMock, patch

import pytest

from bytebite.graph import build_v01_graph
from bytebite.schemas import FoodItem
from bytebite.state import MealAnalysis, merge_unique_logs


# ---------------------------------------------------------------------------
# Baseline Lesson 01 Tests (Passing out-of-the-box)
# ---------------------------------------------------------------------------

def test_idempotent_reducer_deduplicates_retries():
    logs = merge_unique_logs(["[A] ok"], ["[A] ok", "[B] ok"])
    assert logs == ["[A] ok", "[B] ok"]


@patch("bytebite.nodes.get_gemini4")
def test_high_kcal_triggers_warning(mock_get_llm):
    item = FoodItem(name="Fried Pork", est_kcal=920, cook_method="deep_fried")
    fake = MealAnalysis(items=[item], total_est_kcal=920)
    m = MagicMock()
    m.with_structured_output.return_value.invoke.return_value = {
        "parsed": fake,
        "raw": MagicMock(usage_metadata={"total_tokens": 120}),
    }
    m.invoke.return_value = MagicMock(
        content="Swap for steamed fish",
        usage_metadata={"total_tokens": 95},
    )
    mock_get_llm.return_value = m

    out = build_v01_graph().invoke(
        {"meal_input": "x", "user_goal": "cut", "user_allergies": []}
    )
    assert "[Warning] Flagged high risk" in out["audit_logs"]
    assert out["total_tokens"] == 215


# ---------------------------------------------------------------------------
# Homework Lab #1 Required Tests (Unskip & pass all 4!)
# ---------------------------------------------------------------------------

@pytest.mark.skip(reason="TODO (HW1): Remove this skip after implementing 3-way safety router")
@patch("bytebite.nodes.get_gemini4")
def test_1_allergen_short_circuit(mock_get_llm):
    """Priority 1 wins over high kcal: routes to allergen_halt -> END, advisor NEVER called."""
    # Input: user_allergies=['Peanut'], item has allergens=['peanut'] AND kcal=1200.
    # Assert: out['blocked'] is True, 'peanut' in out['matched_allergens'],
    #         and mock_get_llm.return_value.invoke.assert_not_called()!
    raise NotImplementedError


@pytest.mark.skip(reason="TODO (HW1): Remove this skip after implementing 3-way safety router")
@patch("bytebite.nodes.get_gemini4")
def test_2_high_kcal_no_allergy(mock_get_llm):
    """kcal=950, user_allergies=['shellfish'], item allergens=[]: '[Warning]' AND '[Advisor]' in logs."""
    raise NotImplementedError


@pytest.mark.skip(reason="TODO (HW1): Remove this skip after implementing 3-way safety router")
@patch("bytebite.nodes.get_gemini4")
def test_3_clean_meal_direct(mock_get_llm):
    """kcal=480, steamed fish, 0 allergies: len(audit_logs) == 2 (no Warning)."""
    raise NotImplementedError


@pytest.mark.skip(reason="TODO (HW1): Remove this skip after implementing 3-way safety router")
def test_4_retry_log_idempotency():
    """Verify duplicate log strings are deduplicated while preserving insertion order."""
    raise NotImplementedError
