"""Unit tests for Supabase client configuration and connection status handling."""

from __future__ import annotations

from urllib.error import HTTPError

from config import Settings
from database import supabase_db


def _settings(*, url: str | None, key: str | None) -> Settings:
    return Settings(
        app_name="Test Application",
        app_host="127.0.0.1",
        app_port=8080,
        app_reload=False,
        supabase_url=url,
        supabase_key=key,
        supabase_secret_key=None,
    )



def test_status_is_not_configured_without_required_values(monkeypatch) -> None:
    """No remote request is made before both Supabase settings are available."""
    monkeypatch.setattr(supabase_db, "settings", _settings(url=None, key=None))
    supabase_db.clear_supabase_status_cache()

    status = supabase_db.get_supabase_status()

    assert status.state is supabase_db.SupabaseConnectionState.NOT_CONFIGURED


def test_status_reports_success_for_accepted_auth_settings(monkeypatch) -> None:
    """A successful public Auth settings response means the project is reachable."""
    class FakeResponse:
        status = 200

        def __enter__(self):
            return self

        def __exit__(self, *_args) -> None:
            return None

    monkeypatch.setattr(
        supabase_db,
        "settings",
        _settings(url="https://example.supabase.co", key="sb_publishable_test"),
    )
    monkeypatch.setattr(supabase_db, "get_supabase_client", lambda: object())
    monkeypatch.setattr(supabase_db, "urlopen", lambda *_args, **_kwargs: FakeResponse())
    supabase_db.clear_supabase_status_cache()

    status = supabase_db.get_supabase_status(force_refresh=True)

    assert status.state is supabase_db.SupabaseConnectionState.CONNECTED
    assert status.label == "Connected"


def test_status_does_not_expose_key_when_credentials_are_rejected(monkeypatch) -> None:
    """Credential failures remain user-safe and never include the configured key."""
    key = "sb_publishable_sensitive_value"
    monkeypatch.setattr(
        supabase_db,
        "settings",
        _settings(url="https://example.supabase.co", key=key),
    )
    monkeypatch.setattr(supabase_db, "get_supabase_client", lambda: object())

    def reject_request(*_args, **_kwargs):
        raise HTTPError("https://example.supabase.co", 401, "Unauthorized", None, None)

    monkeypatch.setattr(supabase_db, "urlopen", reject_request)
    supabase_db.clear_supabase_status_cache()

    status = supabase_db.get_supabase_status(force_refresh=True)

    assert status.state is supabase_db.SupabaseConnectionState.INVALID_CREDENTIALS
    assert key not in status.message
