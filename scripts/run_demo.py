"""Live streaming execution & Mermaid PNG export for ByteBite v0.1."""

from pathlib import Path

from bytebite.graph import build_v01_graph


def main() -> None:
    app = build_v01_graph()

    # 1. Export visual architecture diagram for GitHub / PR
    assets_dir = Path("assets")
    assets_dir.mkdir(exist_ok=True)
    try:
        png_bytes = app.get_graph().draw_mermaid_png()
        out_png = assets_dir / "v01_graph.png"
        out_png.write_bytes(png_bytes)
        print(f"Saved topology diagram -> {out_png}")
    except Exception as exc:
        print(f"[Info] Skipped Mermaid PNG render (offline or missing renderer): {exc}")

    # 2. Stream per-node state deltas with recursion_limit circuit breaker
    inputs = {
        "meal_input": "Double fried chicken + large brown sugar bubble tea",
        "user_goal": "Dinner <= 550 kcal, high protein",
        "user_allergies": [],
        "total_tokens": 0,
        "audit_logs": [],
    }
    print("\n--- STREAMING BYTEBITE v0.1 ---")
    final_state = dict(inputs)
    for step in app.stream(
        inputs,
        stream_mode="updates",
        config={"recursion_limit": 10},
    ):
        node, delta = next(iter(step.items()))
        print(f">>> [{node}] delta keys: {list(delta.keys())}")
        if "analysis" in delta:
            a = delta["analysis"]
            print(f"    items={len(a.items)}, est_kcal={a.total_est_kcal}")
        if "risk_alert" in delta:
            print(f"    ALERT: {delta['risk_alert']}")
        final_state.update(delta)

    print("\n--- FINAL ADVICE ---")
    print(final_state.get("final_advice", "(none)"))
    print("\n--- FINAL AUDIT TRAIL ---")
    print(final_state.get("audit_logs", []))


if __name__ == "__main__":
    main()
