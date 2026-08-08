"""Environment-backed configuration for the web application."""

from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache

from dotenv import load_dotenv


load_dotenv()


def _read_port(value: str | None, default: int = 8080) -> int:
    """Read a valid TCP port without exposing configuration errors to the UI."""
    try:
        port = int(value or default)
    except ValueError:
        return default
    return port if 1 <= port <= 65535 else default


def _read_bool(value: str | None, default: bool = False) -> bool:
    """Convert a conventional environment boolean to a Python boolean."""
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Settings:
    """Runtime settings loaded from environment variables."""

    app_name: str
    app_host: str
    app_port: int
    app_reload: bool
    supabase_url: str | None
    supabase_key: str | None

    @property
    def supabase_configured(self) -> bool:
        """Whether both required Supabase values have been supplied."""
        return bool(self.supabase_url and self.supabase_key)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Create and cache application settings; no remote connection is made here."""
    return Settings(
        app_name=os.getenv("APP_NAME", "QR Management System"),
        app_host=os.getenv("APP_HOST", "127.0.0.1"),
        app_port=_read_port(os.getenv("APP_PORT")),
        app_reload=_read_bool(os.getenv("APP_RELOAD")),
        supabase_url=os.getenv("SUPABASE_URL") or None,
        supabase_key=os.getenv("SUPABASE_KEY") or None,
    )


settings = get_settings()
