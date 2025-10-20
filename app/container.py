# app/container.py
from __future__ import annotations

from typing import Optional

# Use the same import style as your config (core.*)
from app.core.config import (
    require_openai,
    OPENAI_API_KEY,
    DOWNLOADS_DIR,
)

# --- Services (use cases)
from app.features.rewriting.service import RewriteService

# --- Providers (adapters)
from app.providers.openai_chat import OpenAIChatRewriter

# ---------- Provider singletons (created once) ----------
# These depend only on env/config and are shared by services.

_rewrite_provider = (
    OpenAIChatRewriter(require_openai()) if OPENAI_API_KEY else None
)


# ---------- Factory functions (FastAPI Depends targets) ----------
def get_rewrite_service() -> RewriteService:
    if not _rewrite_provider:
        raise RuntimeError(
            "Rewrite provider not configured. Set OPENAI_API_KEY in .env"
        )
    return RewriteService(_rewrite_provider)
