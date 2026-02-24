"""
config.py - Central configuration for the Career Assistant Platform.

Supports:
  - OpenAI (gpt-3.5-turbo / gpt-4o-mini) via OPENAI_API_KEY
  - HuggingFace Inference API via HF_API_KEY
  - Groq API (free, fast) via GROQ_API_KEY  <-- recommended for free tier users

Set your chosen provider and key in a .env file or Streamlit secrets.
"""

import os
from dotenv import load_dotenv

load_dotenv()  # loads from .env file if present

# ── Provider Selection ────────────────────────────────────────────────────────
# Options: "openai" | "groq" | "huggingface"
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "groq")

# ── API Keys ──────────────────────────────────────────────────────────────────
OPENAI_API_KEY   = os.getenv("OPENAI_API_KEY", "")
GROQ_API_KEY     = os.getenv("GROQ_API_KEY", "")
HF_API_KEY       = os.getenv("HF_API_KEY", "")

# ── Model Names ───────────────────────────────────────────────────────────────
OPENAI_MODEL     = os.getenv("OPENAI_MODEL",  "gpt-4o-mini")
GROQ_MODEL       = os.getenv("GROQ_MODEL",    "llama-3.3-70b-versatile")
HF_MODEL         = os.getenv("HF_MODEL",      "mistralai/Mistral-7B-Instruct-v0.2")

# ── Generation Parameters ─────────────────────────────────────────────────────
MAX_TOKENS       = int(os.getenv("MAX_TOKENS", "2048"))
TEMPERATURE      = float(os.getenv("TEMPERATURE", "0.7"))
