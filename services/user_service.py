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