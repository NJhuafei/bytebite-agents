"""Conditional routing and StateGraph compilation for ByteBite v0.1."""

from typing import Literal

from langgraph.graph import END, START, StateGraph

from bytebite.nodes import (
    advisor_node,
    allergen_halt_node,
    analyzer_node,
    warning_node,
)
from bytebite.state import ByteBiteState


def route_after_analysis(
    state: ByteBiteState,
) -> Literal["warning_node", "advisor"]:
    """Lesson 01 baseline 2-way router (no allergy short-circuit yet!)."""
    a = state["analysis"]
    fried_cnt = sum(i.cook_method == "deep_fried" for i in a.items)
    if fried_cnt >= 2 or a.total_est_kcal > 850:
        return "warning_node"
    return "advisor"


def route_safety_3way(
    state: ByteBiteState,
) -> Literal["allergen_halt", "warning_node", "advisor"]:
    """TODO (HW1): Upgrade to a 3-way priority safety router.

    Priority 1: Any case-insensitive overlap between state.get('user_allergies', [])
                and any item.allergens -> 'allergen_halt'
    Priority 2: deep_fried >= 2 or total_est_kcal > 850 -> 'warning_node'
    Priority 3: Otherwise -> 'advisor'
    """
    raise NotImplementedError("TODO (HW1): Implement route_safety_3way in bytebite/graph.py")


def build_v01_graph():
    """Compile the Lesson 01 ByteBite StateGraph.

    TODO (HW1): Register 'allergen_halt' -> allergen_halt_node, switch the
    conditional edge to route_safety_3way, and wire 'allergen_halt' directly to END!
    """
    g = StateGraph(ByteBiteState)
    g.add_node("analyzer", analyzer_node)
    g.add_node("warning_node", warning_node)
    g.add_node("advisor", advisor_node)

    g.add_edge(START, "analyzer")
    g.add_conditional_edges("analyzer", route_after_analysis)
    g.add_edge("warning_node", "advisor")
    g.add_edge("advisor", END)
    return g.compile()
