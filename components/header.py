"""Shared application header."""

from nicegui import ui


def render_header() -> None:
    """Render the top toolbar for the unauthenticated shell state."""
    with ui.row().classes("w-full items-center no-wrap px-4"):
        ui.label("QR Management System").classes("text-h6 text-weight-bold")
        ui.space()
        ui.icon("account_circle").classes("text-2xl")
        ui.label("Demo Operator").classes("text-body2 ml-1")
        ui.button("Logout", icon="logout", on_click=lambda: ui.navigate.to("/login")).props(
            "flat no-caps"
        ).classes("ml-3")
