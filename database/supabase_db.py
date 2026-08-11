"""Supabase client construction and non-invasive connectivity checks."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from enum import Enum
from functools import lru_cache
from threading import Lock
from time import monotonic
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from supabase import Client, create_client

from config import settings


logger = logging.getLogger(__name__)

_HEALTHCHECK_TIMEOUT_SECONDS = 5
_STATUS_CACHE_SECONDS = 30
_status_lock = Lock()
_cached_status: tuple[float, "SupabaseConnectionStatus"] | None = None


class SupabaseConnectionState(str, Enum):
    """Connection states that are safe to present in the application UI."""

    CONNECTED = "connected"
    NOT_CONFIGURED = "not_configured"
    UNAVAILABLE = "unavailable"
    INVALID_CREDENTIALS = "invalid_credentials"


@dataclass(frozen=True)
class SupabaseConnectionStatus:
    """The result of a Supabase availability check."""

    state: SupabaseConnectionState
    message: str

    @property
    def label(self) -> str:
        """Return the concise status text displayed in the footer."""
        labels = {
            SupabaseConnectionState.CONNECTED: "Connected",
            SupabaseConnectionState.NOT_CONFIGURED: "Not configured",
            SupabaseConnectionState.UNAVAILABLE: "Unavailable",
            SupabaseConnectionState.INVALID_CREDENTIALS: "Credentials rejected",
        }
        return labels[self.state]


class SupabaseConfigurationError(RuntimeError):
    """Raised when the requested Supabase client is not configured."""


@lru_cache(maxsize=2)
def get_supabase_client(*, use_secret_key: bool = False) -> Client:
    """Create a cached Supabase client using the requested server-side key."""

    if not settings.supabase_url:
        raise SupabaseConfigurationError(
            "SUPABASE_URL must be configured before creating a client."
        )

    if use_secret_key:
        if not settings.supabase_secret_key:
            raise SupabaseConfigurationError(
                "SUPABASE_SECRET_KEY must be configured for admin operations."
            )
        key = settings.supabase_secret_key
    else:
        if not settings.supabase_key:
            raise SupabaseConfigurationError(
                "SUPABASE_KEY must be configured before creating a client."
            )
        key = settings.supabase_key

    # Keys are deliberately never logged or returned to the UI.
    return create_client(settings.supabase_url, key)


def get_supabase_status(*, force_refresh: bool = False) -> SupabaseConnectionStatus:
    """Check whether Supabase accepts the configured public application credentials.

    The check calls the public Auth settings endpoint only. It does not query
    application tables, create sessions, or mutate any Supabase data.
    """
    global _cached_status

    if not settings.supabase_configured:
        return SupabaseConnectionStatus(
            SupabaseConnectionState.NOT_CONFIGURED,
            "Supabase URL or public key has not been configured.",
        )

    now = monotonic()
    with _status_lock:
        if (
            not force_refresh
            and _cached_status is not None
            and now - _cached_status[0] < _STATUS_CACHE_SECONDS
        ):
            return _cached_status[1]

        status = _check_supabase_connection()
        _cached_status = (now, status)
        return status


def clear_supabase_status_cache() -> None:
    """Clear the in-memory health cache; useful for tests and future refresh actions."""
    global _cached_status
    with _status_lock:
        _cached_status = None


def _check_supabase_connection() -> SupabaseConnectionStatus:
    """Perform the low-level, read-only Supabase availability request."""
    assert settings.supabase_url is not None
    assert settings.supabase_key is not None

    try:
        # Build the official client first so invalid client configuration is caught early.
        get_supabase_client()
        endpoint = f"{settings.supabase_url.rstrip('/')}/auth/v1/settings"
        request = Request(
            endpoint,
            headers={
                "apikey": settings.supabase_key,
                "Authorization": f"Bearer {settings.supabase_key}",
            },
            method="GET",
        )
        with urlopen(request, timeout=_HEALTHCHECK_TIMEOUT_SECONDS) as response:
            if 200 <= response.status < 300:
                return SupabaseConnectionStatus(
                    SupabaseConnectionState.CONNECTED,
                    "Supabase is reachable and accepted the configured public credentials.",
                )

        return SupabaseConnectionStatus(
            SupabaseConnectionState.UNAVAILABLE,
            "Supabase returned an unexpected response.",
        )
    except HTTPError as error:
        if error.code in {401, 403}:
            logger.warning("Supabase rejected the configured public credentials.")
            return SupabaseConnectionStatus(
                SupabaseConnectionState.INVALID_CREDENTIALS,
                "Supabase rejected the configured public key.",
            )
        logger.warning("Supabase health check returned HTTP %s.", error.code)
    except (TimeoutError, URLError, OSError):
        logger.warning("Supabase health check could not reach the configured project.")
    except Exception:
        # Do not log the exception text here: configuration exceptions can include
        # request details, and credentials must never reach application logs.
        logger.error("Supabase client setup or connectivity check failed.")

    return SupabaseConnectionStatus(
        SupabaseConnectionState.UNAVAILABLE,
        "Unable to connect to Supabase. Check the project URL, key, and network connection.",
    )
