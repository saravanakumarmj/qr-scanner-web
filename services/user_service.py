"""Application user management."""

from __future__ import annotations

from typing import Any

from database.supabase_db import get_supabase_client
from config import settings


AUTH_EMAIL_DOMAIN = "qr-management.local"

VALID_ROLES = {"ADMIN", "OPERATOR", "VIEWER"}


def build_auth_email(user_id: str) -> str:
    """Build the internal email used only by Supabase Auth."""
    normalized = user_id.strip().lower()

    if not normalized:
        raise ValueError("User ID is required.")

    return f"{normalized}@{AUTH_EMAIL_DOMAIN}"


def create_user(
    user_id: str,
    password: str,
    full_name: str,
    role: str,
) -> dict[str, Any]:
    """Create a Supabase Auth user and corresponding application user."""

    if not settings.supabase_admin_configured:
        raise RuntimeError("Supabase secret key is not configured.")

    user_id = user_id.strip()
    full_name = full_name.strip()
    role = role.strip().upper()

    if not user_id:
        raise ValueError("User ID is required.")

    if not password:
        raise ValueError("Password is required.")

    if not full_name:
        raise ValueError("Full name is required.")

    if role not in VALID_ROLES:
        raise ValueError(f"Invalid role: {role}")

    auth_email = build_auth_email(user_id)

    admin_client = get_supabase_client(use_secret_key=True)

    # 1. Create the Supabase Auth identity.
    auth_response = admin_client.auth.admin.create_user(
        {
            "email": auth_email,
            "password": password,
            "email_confirm": True,
        }
    )

    auth_user = auth_response.user

    if auth_user is None:
        raise RuntimeError("Supabase Auth user creation failed.")

    # 2. Create the application user.
    try:
        response = (
            admin_client.table("app_users")
            .insert(
                {
                    "auth_user_id": str(auth_user.id),
                    "user_id": user_id,
                    "full_name": full_name,
                    "role": role,
                    "is_active": True,
                }
            )
            .execute()
        )
    except Exception:
        # Do not leave an orphan Auth account.
        try:
            admin_client.auth.admin.delete_user(str(auth_user.id))
        except Exception:
            pass
        raise

    if not response.data:
        raise RuntimeError("Application user creation failed.")

    return response.data[0]


def list_users() -> list[dict[str, Any]]:
    """Return all application users."""

    client = get_supabase_client()

    response = (
        client.table("app_users")
        .select(
            "id,auth_user_id,user_id,full_name,role,is_active,"
            "created_at,updated_at,location"
        )
        .order("user_id")
        .execute()
    )

    return response.data or []


def update_user(
    auth_user_id: str,
    full_name: str,
    role: str,
    location: str | None,
) -> dict[str, Any]:
    """Update application user details."""

    if not settings.supabase_admin_configured:
        raise RuntimeError("Supabase secret key is not configured.")

    auth_user_id = auth_user_id.strip()
    full_name = full_name.strip()
    role = role.strip().upper()
    location = (location or "").strip() or None

    if not auth_user_id:
        raise ValueError("Auth user ID is required.")

    if not full_name:
        raise ValueError("Full name is required.")

    if role not in VALID_ROLES:
        raise ValueError(f"Invalid role: {role}")

    admin_client = get_supabase_client(use_secret_key=True)

    response = (
        admin_client.table("app_users")
        .update(
            {
                "full_name": full_name,
                "role": role,
                "location": location,
            }
        )
        .eq("auth_user_id", auth_user_id)
        .execute()
    )

    if not response.data:
        raise RuntimeError("User update failed.")

    return response.data[0]


def set_user_active(
    auth_user_id: str,
    is_active: bool,
) -> dict[str, Any]:
    """Activate or deactivate an application user."""

    if not settings.supabase_admin_configured:
        raise RuntimeError("Supabase secret key is not configured.")

    auth_user_id = auth_user_id.strip()

    if not auth_user_id:
        raise ValueError("Auth user ID is required.")

    admin_client = get_supabase_client(use_secret_key=True)

    response = (
        admin_client.table("app_users")
        .update({"is_active": is_active})
        .eq("auth_user_id", auth_user_id)
        .execute()
    )

    if not response.data:
        raise RuntimeError("Unable to update user status.")

    return response.data[0]


def reset_user_password(
    auth_user_id: str,
    new_password: str,
) -> None:
    """Reset a user's Supabase Auth password."""

    if not settings.supabase_admin_configured:
        raise RuntimeError("Supabase secret key is not configured.")

    auth_user_id = auth_user_id.strip()
    new_password = new_password.strip()

    if not auth_user_id:
        raise ValueError("Auth user ID is required.")

    if not new_password:
        raise ValueError("Password is required.")

    if len(new_password) < 6:
        raise ValueError(
            "Password must be at least 6 characters."
        )

    admin_client = get_supabase_client(use_secret_key=True)

    response = admin_client.auth.admin.update_user_by_id(
        auth_user_id,
        {
            "password": new_password,
        },
    )

    if response.user is None:
        raise RuntimeError("Password reset failed.")