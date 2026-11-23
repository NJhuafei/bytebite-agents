"""Centralized Gemini 4 tiered model factory with thinking_level control."""

import os
from typing import Literal

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

ModelTier = Literal["fast_scout", "balanced", "deep_debate"]

TIER_CONFIG: dict[ModelTier, tuple[str, str, float]] = {
    # (model_id, thinking_level, temperature)
    "fast_scout": ("gemini-4-hydrogen", "low", 0.0),
    "balanced": ("gemini-4-neon", "medium", 0.2),
    "deep_debate": ("gemini-4-argon", "high", 0.3),
}


def get_gemini4(tier: ModelTier = "fast_scout") -> ChatGoogleGenerativeAI:
    """Return a configured Gemini 4 client for the requested reasoning tier."""
    model_id, effort, temp = TIER_CONFIG[tier]
    return ChatGoogleGenerativeAI(
        model=model_id,
        temperature=temp,
        timeout=20.0,
        max_retries=2,
        model_kwargs={"thinking_level": effort},
        api_key=os.environ["GEMINI_API_KEY"],
    )
