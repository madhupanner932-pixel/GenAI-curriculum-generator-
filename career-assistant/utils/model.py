"""
utils/model.py

Single entry-point for all LLM calls across every module.
  query_model(system_prompt, user_input) -> str
"""

import os
import requests
import streamlit as st
from config import (
    LLM_PROVIDER, OPENAI_API_KEY, GROQ_API_KEY, HF_API_KEY,
    OPENAI_MODEL, GROQ_MODEL, HF_MODEL,
    MAX_TOKENS, TEMPERATURE
)


# ── Helper: resolve key from Streamlit secrets or env ────────────────────────
def _resolve_key(env_key: str, secret_key: str) -> str:
    """Return key from st.secrets first, then env, then empty string."""
    try:
        return st.secrets.get(secret_key, "") or env_key
    except Exception:
        return env_key


# ── OpenAI / compatible (Groq uses same SDK format) ──────────────────────────
def _call_openai_compatible(base_url: str, api_key: str, model: str,
                             system_prompt: str, user_input: str) -> str:
    import openai
    client = openai.OpenAI(api_key=api_key, base_url=base_url)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system",  "content": system_prompt},
            {"role": "user",    "content": user_input},
        ],
        max_tokens=MAX_TOKENS,
        temperature=TEMPERATURE,
    )
    return response.choices[0].message.content.strip()


# ── HuggingFace Inference API ─────────────────────────────────────────────────
def _call_huggingface(system_prompt: str, user_input: str) -> str:
    api_key = _resolve_key(HF_API_KEY, "HF_API_KEY")
    url = f"https://api-inference.huggingface.co/models/{HF_MODEL}"
    headers = {"Authorization": f"Bearer {api_key}"}
    payload = {
        "inputs": f"<s>[INST] <<SYS>>\n{system_prompt}\n<</SYS>>\n\n{user_input} [/INST]",
        "parameters": {"max_new_tokens": MAX_TOKENS, "temperature": TEMPERATURE},
    }
    resp = requests.post(url, headers=headers, json=payload, timeout=60)
    resp.raise_for_status()
    data = resp.json()
    if isinstance(data, list) and data:
        return data[0].get("generated_text", "").strip()
    raise ValueError(f"Unexpected HuggingFace response: {data}")


# ── Public function ───────────────────────────────────────────────────────────
def query_model(system_prompt: str, user_input: str) -> str:
    """
    Universal LLM query function used by all modules.

    Parameters
    ----------
    system_prompt : str  – Role/context instructions for the model.
    user_input    : str  – The user's request or input text.

    Returns
    -------
    str – The model's text response.
    """
    provider = LLM_PROVIDER.lower()

    try:
        if provider == "openai":
            api_key = _resolve_key(OPENAI_API_KEY, "OPENAI_API_KEY")
            return _call_openai_compatible(
                "https://api.openai.com/v1", api_key, OPENAI_MODEL,
                system_prompt, user_input
            )

        elif provider == "groq":
            api_key = _resolve_key(GROQ_API_KEY, "GROQ_API_KEY")
            return _call_openai_compatible(
                "https://api.groq.com/openai/v1", api_key, GROQ_MODEL,
                system_prompt, user_input
            )

        elif provider == "huggingface":
            return _call_huggingface(system_prompt, user_input)

        else:
            return f"❌ Unknown provider '{provider}'. Set LLM_PROVIDER to openai, groq, or huggingface."

    except Exception as e:
        return f"❌ Model error ({provider}): {str(e)}"
