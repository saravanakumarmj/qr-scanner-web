"""Shared application footer."""

from nicegui import ui

from config import settings


def render_footer() -> None:
    """Render runtime status labels without attempting any external connection."""
    supabase_status = "Configured" if settings.supabase_configured else "Not configured"
    with ui.row().classes("w-full items-center gap-6 px-5 py-2 text-caption"):
        ui.label(f"Supabase: {supabase_status}")
        ui.label("Printer: Not configured")
        ui.label("User: Demo Operator")
