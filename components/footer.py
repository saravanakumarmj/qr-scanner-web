"""Shared application footer."""

from nicegui import app, ui

from config import settings
from database.supabase_db import get_supabase_status


def get_printer_status() -> str:
    """Return the current configured printer status."""

    if not settings.printer_name:
        return "Not configured"

    try:
        import win32print

        handle = win32print.OpenPrinter(settings.printer_name)

        try:
            info = win32print.GetPrinter(handle, 2)
            attributes = info["Attributes"]

            # Zebra ZD230 USB driver reports this bit when
            # the physical printer is switched off.
            if attributes & 1024:
                return "Not connected"

            return "Connected"

        finally:
            win32print.ClosePrinter(handle)

    except Exception:
        return "Not connected"

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

    with ui.row().classes(
        "w-full items-center gap-6 px-5 py-2 text-caption"
    ):
        ui.label(
            f"Supabase: {supabase_status.label}"
        ).tooltip(
            supabase_status.message
        )

        ui.label(
            f"Printer: {printer_status}"
        )

        ui.label(
            f"User: {user_name}"
        )