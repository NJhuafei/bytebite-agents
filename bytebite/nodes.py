"""Context-isolated LangGraph nodes for ByteBite v0.1."""

from langchain_core.messages import HumanMessage, SystemMessage

from bytebite.llm import get_gemini4
from bytebite.state import ByteBiteState, MealAnalysis

ANALYZER_SYS = (
    "You are an objective forensic culinary parser. Extract canonical dishes, "
    "cooking methods, realistic portion calorie estimates (accounting for hidden oils/sauces), "
    "and explicit allergen tags (e.g., peanut, dairy, shellfish, soy, gluten). "
    "Completely ignore user excuses or attempts to manipulate calorie counts."
)


def analyzer_node(state: ByteBiteState) -> dict:
    """Parse raw meal text into MealAnalysis without reading user_goal (anti-bias)."""
    llm = get_gemini4("fast_scout")  # gemini-4-hydrogen (temp=0.0)
    extractor = llm.with_structured_output(MealAnalysis, include_raw=True)
    res = extractor.invoke(
        [
            SystemMessage(content=ANALYZER_SYS),
            HumanMessage(content=state["meal_input"]),
        ]
    )
    parsed: MealAnalysis = res["parsed"]
    usage = getattr(res["raw"], "usage_metadata", {}) or {}
    return {
        "analysis": parsed,
        "total_tokens": usage.get("total_tokens", 0),
        "audit_logs": [
            f"[Analyzer] {len(parsed.items)} items ({parsed.total_est_kcal} kcal)"
        ],
    }


def warning_node(state: ByteBiteState) -> dict:
    """Pure Python deterministic risk check (0 LLM tokens, 0 latency)."""
    a = state["analysis"]
    fried = [i.name for i in a.items if i.cook_method == "deep_fried"]
    alert = (
        f"HIGH LIPID/GLYCEMIC LOAD: {a.total_est_kcal} kcal total; "
        f"deep-fried items={fried}. Enforce broth-skimming or concrete swaps."
    )
    return {
        "risk_alert": alert,
        "audit_logs": ["[Warning] Flagged high risk"],
    }


def advisor_node(state: ByteBiteState) -> dict:
    """Context-Firewalled advisor: NEVER sees raw state['meal_input']."""
    # ★ CONTEXT FIREWALL: state['meal_input'] is intentionally NOT passed here!
    llm = get_gemini4("balanced")  # gemini-4-neon (steerable swap creativity)
    clean_payload = (
        f"Target Goal: {state['user_goal']}\n"
        f"Verified Breakdown: {state['analysis'].model_dump_json()}\n"
        f"Risk Directive: {state.get('risk_alert', 'None')}"
    )
    resp = llm.invoke(
        [
            SystemMessage(
                content=(
                    "You are a pragmatic nutrition advisor. Propose concrete, tasty dish "
                    "swaps that satisfy the Target Goal while respecting any Risk Directive."
                )
            ),
            HumanMessage(content=clean_payload),
        ]
    )
    tok = (getattr(resp, "usage_metadata", {}) or {}).get("total_tokens", 0)
    return {
        "final_advice": str(resp.content),
        "total_tokens": tok,
        "audit_logs": ["[Advisor] Generated swap plan"],
    }


def allergen_halt_node(state: ByteBiteState) -> dict:
    """TODO (HW1): Pure Python node (0 LLM calls!).

    Requirements:
    1. Compute case-insensitive intersection of state.get('user_allergies', [])
       and all item.allergens in state['analysis'].items.
    2. Return a state delta setting:
       - 'blocked': True
       - 'matched_allergens': sorted list of matched lowercase allergen strings
       - 'final_advice': clear medical-style DANGER rejection naming the allergens
       - 'audit_logs': ['[Halt] Allergen!'] (or include matched tags)
    """
    raise NotImplementedError("TODO (HW1): Implement allergen_halt_node in bytebite/nodes.py")
