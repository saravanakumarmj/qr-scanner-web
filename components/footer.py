"""Shared application footer."""

from nicegui import app, ui

from config import settings
from database.supabase_db import get_supabase_status
from services.printer_service import get_printer_status




def get_current_user() -> str:
    """Return the currently logged-in user."""

    user = app.storage.user.get("user") or {}

    return (
        user.get("full_name")
        or user.get("user_id")
        or "Unknown"
    )


def render_footer() -> None:
    """Render runtime status labels."""

    supabase_status = get_supabase_status()
    printer_status = get_printer_status()
    user_name = get_current_user()

    printer_label = (
        "Connected"
        if printer_status["connected"]
        else "Not connected"
    )

    with ui.row().classes(
        "w-full items-center gap-6 px-5 py-2 text-caption"
    ):
        ui.label(
            f"Supabase: {supabase_status.label}"
        ).tooltip(
            supabase_status.message
        )

        ui.label(
            f"Printer: {printer_label}"
        ).tooltip(
            printer_status["message"]
        )

        ui.label(
            f"User: {user_name}"
        )