"""Shared left navigation drawer."""

from __future__ import annotations

from nicegui import ui


def _navigation_button(label: str, icon: str, path: str, key: str, active_key: str) -> None:
    """Add a navigation button and highlight the active destination."""
    button = ui.button(label, icon=icon, on_click=lambda destination=path: ui.navigate.to(destination))
    button.props("flat no-caps align=left")
    button.classes("nav-entry w-full justify-start px-4")
    if key == active_key:
        button.classes("bg-blue-8 text-white")
    else:
        button.classes("text-blue-grey-1")


def render_navigation(active_key: str) -> None:
    """Render the shared navigation hierarchy."""
    with ui.column().classes("w-full gap-1 p-3"):
        with ui.row().classes("items-center gap-2 px-3 py-3"):
            ui.icon("qr_code_2").classes("text-3xl text-cyan-3")
            ui.label("CAN MANAGEMENT System").classes("text-subtitle1 text-weight-bold tracking-wide")
        ui.separator().classes("bg-blue-grey-7 mb-2")
        _navigation_button("Dashboard", "dashboard", "/dashboard", "dashboard", active_key)

        with ui.expansion("Operations", icon="precision_manufacturing", value=active_key in {"generate", "reprint", "discard", "print_history"}).classes("w-full text-white"):
            with ui.column().classes("w-full gap-1 pl-3"):
                _navigation_button("Generate QR", "add_circle_outline", "/operations/generate", "generate", active_key)
                _navigation_button("Reprint QR", "replay", "/operations/reprint", "reprint", active_key)
                _navigation_button("Discard QR", "delete_outline", "/operations/discard", "discard", active_key)
                _navigation_button("Print History", "history", "/operations/print-history", "print_history", active_key)

        _navigation_button("Reports", "assessment", "/reports", "reports", active_key)

        with ui.expansion("Administration", icon="admin_panel_settings", value=active_key in {"users", "devices", "locations", "printers", "settings", "audit_log"}).classes("w-full text-white"):
            with ui.column().classes("w-full gap-1 pl-3"):
                _navigation_button("Users", "group", "/administration/users", "users", active_key)
                _navigation_button("Devices", "devices", "/administration/devices", "devices", active_key)
                _navigation_button("Locations", "location_on", "/administration/locations", "locations", active_key)
                _navigation_button("Printers", "print", "/administration/printers", "printers", active_key)
                _navigation_button("System Settings", "settings", "/administration/settings", "settings", active_key)
                _navigation_button("Audit Log", "fact_check", "/administration/audit-log", "audit_log", active_key)

        ui.separator().classes("bg-blue-grey-7 my-2")
        _navigation_button("Profile", "account_circle", "/profile", "profile", active_key)
