import logging
import sys
import os

from typing import List, Optional

from app.core.logging import InterceptHandler
from loguru import logger
from starlette.config import Config
from starlette.datastructures import Secret

config = Config(".env")

API_PREFIX = "/api"
VERSION = "0.1.0"
DEBUG: bool = config("DEBUG", cast=bool, default=False)

PROJECT_NAME: str = config("PROJECT_NAME", default="test-py-fastapi")

OPENAI_API_KEY: Optional[Secret] = config("OPENAI_API_KEY", cast=Secret, default=None)

DOWNLOADS_DIR: str = config("DOWNLOADS_DIR", default="downloads")
os.makedirs(DOWNLOADS_DIR, exist_ok=True)

#CORS_ORIGINS="http://localhost:3000,https://your.site"
_raw_cors = config("CORS_ORIGINS", default="")
CORS_ORIGINS: List[str] = [o.strip() for o in _raw_cors.split(",") if o.strip()]

# logging configuration
LOGGING_LEVEL = logging.DEBUG if DEBUG else logging.INFO
logging.basicConfig(
    handlers=[InterceptHandler(level=LOGGING_LEVEL)], level=LOGGING_LEVEL
)
logger.configure(handlers=[{"sink": sys.stderr, "level": LOGGING_LEVEL}])


def require_openai() -> str:
    """Return raw OpenAI key or raise helpful error."""
    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY is not configured")
    return str(OPENAI_API_KEY)

