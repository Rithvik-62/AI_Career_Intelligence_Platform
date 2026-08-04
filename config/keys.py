"""
API Configuration Keys
All credentials are loaded exclusively from environment variables or Streamlit Secrets.
NEVER hardcode API keys here — those are configured in Streamlit Cloud Secrets (secrets.toml).
"""

import os
import streamlit as st

def _get_secret(env_key: str, streamlit_key: str = None) -> str:
    """Read from Streamlit secrets first, then OS environment variables."""
    _key = streamlit_key or env_key
    # Try Streamlit Cloud secrets first (preferred when deployed)
    try:
        val = st.secrets.get(_key, "")
        if val:
            return val
    except Exception:
        pass
    # Fall back to OS environment variable (local .env or CI/CD secrets)
    return os.getenv(env_key, "")

GEMINI_API_KEY = _get_secret("GEMINI_API_KEY")
NEWS_API_KEY = _get_secret("NEWS_API_KEY")
