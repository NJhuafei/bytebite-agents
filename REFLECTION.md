# Lesson 01 Architectural Reflection

> **Instructions**: Choose **ANY 2** of the 4 prompts below (150–250 words each).
> Support your argument with concrete Pydantic field definitions, equations, or data from `results/ablation_v01.md`.

---

## Prompt 1: Lossy Bottleneck vs. Context Rot
Context Firewalling hides `meal_input` from `advisor_node`—blocking `TC5` excuses, yet also dropping benign nuances (*"my throat hurts, avoid crispy textures"*). Propose a typed field design in `MealAnalysis` that preserves legitimate physical constraints without re-opening prompt injection.

*(Write your response here if selected)*

---

## Prompt 2: Latency & Token Break-Even Math
Using your Task 2 telemetry, compute `ΔLatency` and `ΔTokens` between Baseline and `v0.1-hw`. Notice `TC2`/`TC3` save tokens via short-circuiting while `TC1` adds a hop! Derive a formula for expected cost `E[Tokens]` as a function of allergy halt rate `p_halt`.

*(Write your response here if selected)*

---

## Prompt 3: 'Validated-Garbage-Out' Paradox
In `TC1`, Pydantic enforces `0 < est_kcal <= 2500`, yet Gemini 4 Hydrogen can still guess `450 kcal` for a `950 kcal` chili-oil bowl! Explain why type validation ≠ factual grounding, and sketch the exact tool-calling architecture needed in Lesson 2.

*(Write your response here if selected)*

---

## Prompt 4: False Positives in Deterministic Halts
Suppose a user says *"Chicken breast, NO peanuts"* and a naive Analyzer extracts `allergens=['peanut']`, triggering a false `allergen_halt`! How would you redesign the `FoodItem` schema (e.g., `present_allergens` vs. `negated_allergens`) to prevent false halts?

*(Write your response here if selected)*
