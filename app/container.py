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
from app.features.images.service import ImageGenService
from app.features.transcription.service import TranscriptService

# --- Providers (adapters)
from app.providers.openai_chat import OpenAIChatRewriter
from app.providers.openai_images import OpenAIImagegen
from app.providers.openai_transcript import OpenAIWhisper

# ---------- Provider singletons (created once) ----------
# These depend only on env/config and are shared by services.

_rewrite_provider = (
    OpenAIChatRewriter(require_openai()) if OPENAI_API_KEY else None
)

_images_provider = (
    OpenAIImagegen(require_openai()) if OPENAI_API_KEY else None
)

_transcription_provider = (
    OpenAIWhisper(require_openai()) if OPENAI_API_KEY else None
)


# ---------- Factory functions (FastAPI Depends targets) ----------
def get_rewrite_service() -> RewriteService:
    if not _rewrite_provider:
        raise RuntimeError(
            "Rewrite provider not configured. Set OPENAI_API_KEY in .env"
        )
    return RewriteService(_rewrite_provider)

def get_image_gen_service() -> ImageGenService:
    if not _images_provider:
        raise RuntimeError(
            "Image Gen provider not configured. Set OPENAI_API_KEY in .env"
        )
    return ImageGenService(_images_provider)

def get_transcription_service() -> TranscriptService:
    if not _transcription_provider:
        raise RuntimeError(
            "Transcription provider not configured. Set OPENAI_API_KEY in .env"
        )
    return TranscriptService(_transcription_provider)
