# ByteBite Multi-Agent AI Engineering (`v0.1` Starter)

Welcome to **ByteBite**! Over 8 progressive lessons (`v0.1` → `v1.0`), you will evolve this repository into a 6-agent multimodal decision system powered by **Gemini 4** (`gemini-4-hydrogen`, `gemini-4-neon`, `gemini-4-argon`), **LangGraph**, and **Pydantic v2**.

## 1. Quickstart (5 Minutes)

```bash
# 1. Install uv (if not already installed): https://docs.astral.sh/uv/
uv sync

# 2. Configure your Gemini API key (NEVER commit .env!)
cp .env.example .env
# Open .env and paste your GEMINI_API_KEY

# 3. Run hermetic offline unit tests (0 network calls, ~50ms)
uv run pytest -q

# 4. Run the live Lesson 01 streaming demo
uv run python scripts/run_demo.py
```

## 2. Repository Layout

```text
bytebite-agents/
├── pyproject.toml           # uv & pytest config
├── .env.example             # API key template
├── .github/workflows/ci.yml # Automated offline pytest CI
├── bytebite/
│   ├── __init__.py
│   ├── schemas.py           # Pydantic v2 FoodItem + allergen validator
│   ├── llm.py               # Gemini 4 tiered factory (Hydrogen / Neon / Argon)
│   ├── state.py             # ByteBiteState + idempotent merge_unique_logs
│   ├── nodes.py             # Analyzer (include_raw), Warning, Context-Firewalled Advisor
│   └── graph.py             # Conditional router & StateGraph compiler
├── scripts/
│   └── run_demo.py          # Streaming delta execution + Mermaid PNG export
├── evals/
│   └── bench_v01.py         # HW Task 2: 5-case ablation benchmark harness
├── tests/
│   └── test_v01.py          # HW Task 1: Hermetic offline pytest suite
└── REFLECTION.md            # HW Task 3: Architectural reflection template
```

## 3. Homework Lab #1 Submission Workflow

1. Create a feature branch: `git checkout -b feat/hw01-3way-safety`
2. Complete **Task 1** (`state.py`, `nodes.py`, `graph.py`, and unskip/pass all 4 HW tests in `tests/test_v01.py`).
3. Complete **Task 2**: run `uv run python evals/bench_v01.py` and write `results/ablation_v01.md`.
4. Complete **Task 3**: answer **2 of 4** prompts in `REFLECTION.md`.
5. Export your updated 3-way graph to `assets/v01_hw_graph.png`.
6. Open a **Draft Pull Request** to `main` 24h before Lesson 02 and tag your instructor for line-by-line Code Review.
7. Once merged, tag your release: `git tag v0.1 && git push origin main --tags`
