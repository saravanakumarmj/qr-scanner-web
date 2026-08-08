"""Shared application footer."""

from nicegui import ui

from database.supabase_db import get_supabase_status


def render_footer() -> None:
    """Render runtime status labels, including the cached Supabase health state."""
    supabase_status = get_supabase_status()
    with ui.row().classes("w-full items-center gap-6 px-5 py-2 text-caption"):
        ui.label(f"Supabase: {supabase_status.label}").tooltip(supabase_status.message)
        ui.label("Printer: Not configured")
        ui.label("User: Demo Operator")
