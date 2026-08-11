"""Authentication service for QR Management System."""

from __future__ import annotations

from dataclasses import dataclass

from config import settings
from database.supabase_db import get_supabase_client
from services.user_service import build_auth_email
from nicegui import app

@dataclass(frozen=True)
class AuthenticatedUser:
    """Application user associated with the current Supabase session."""

    auth_user_id: str
    user_id: str
    full_name: str
    role: str
    is_active: bool


def login(user_id: str, password: str) -> AuthenticatedUser:
    """Authenticate an application user using User ID and password."""

    user_id = user_id.strip()

    if not user_id:
        raise ValueError("User ID is required.")

    if not password:
        raise ValueError("Password is required.")

    client = get_supabase_client()

    # First verify that the application user exists and is active.
    response = (
        client.table("app_users")
        .select("auth_user_id,user_id,full_name,role,is_active")
        .eq("user_id", user_id)
        .limit(1)
        .execute()
    )

    if not response.data:
        raise ValueError("Invalid User ID or password.")

    user = response.data[0]

    if not user["is_active"]:
        raise ValueError("This user account is inactive.")

    # Supabase Auth still uses the internal email.
    auth_email = build_auth_email(user_id)

    auth_response = client.auth.sign_in_with_password(
        {
            "email": auth_email,
            "password": password,
        }
    )

    if auth_response.user is None or auth_response.session is None:
        raise ValueError("Invalid User ID or password.")

    return AuthenticatedUser(
        auth_user_id=str(auth_response.user.id),
        user_id=user["user_id"],
        full_name=user["full_name"],
        role=user["role"],
        is_active=user["is_active"],
    )


def logout() -> None:
    """Sign out the current Supabase session."""
    client = get_supabase_client()
    client.auth.sign_out()


def get_current_session():
    """Return the current Supabase session, if one exists."""
    client = get_supabase_client()
    return client.auth.get_session()


def is_authenticated() -> bool:
    """Return True when the current NiceGUI user is authenticated."""
    try:
        user = app.storage.user.get("user")
        return bool(user and user.get("auth_user_id"))
    except Exception:
        return False



def logout() -> None:
    """Sign out the current user and clear stored login."""

    client = get_supabase_client()
    client.auth.sign_out()

    app.storage.user.pop("user", None)

