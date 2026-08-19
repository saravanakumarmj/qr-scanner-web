"""Shared application footer."""

from nicegui import app, ui

from database.supabase_db import get_supabase_status
from services.printer_service import check_print_agent


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
    user_name = get_current_user()

    # Capture the current NiceGUI client.
    client = ui.context.client

    with ui.row().classes(
        "w-full items-center gap-6 px-5 py-2 text-caption"
    ):
        ui.label(
            f"Supabase: {supabase_status.label}"
        ).tooltip(
            supabase_status.message
        )

        printer_label = ui.label(
            "Printer: Checking..."
        )

        printer_message = ui.label().classes(
            "hidden"
        )

        ui.label(
            f"User: {user_name}"
        )

    async def update_printer_status() -> None:
        """Update the footer with the physical printer status."""

        try:
            printer_status = await check_print_agent(client)

            if printer_status["connected"]:
                printer_label.text = "Printer: Connected"
            else:
                printer_label.text = (
                    f"Printer: {printer_status['status'].replace('_', ' ').title()}"
                )

            printer_label.tooltip(
                printer_status["message"]
            )

        except Exception as exc:
            printer_label.text = "Printer: Unavailable"
            printer_label.tooltip(str(exc))

    # Check immediately.
    ui.timer(
        0.1,
        update_printer_status,
        once=True,
    )

    # Refresh periodically so ON/OFF changes are reflected.
    ui.timer(
        10.0,
        update_printer_status,
    )