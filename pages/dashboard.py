"""Dashboard shell page."""

from nicegui import ui

from components.layout import application_layout


def render_dashboard() -> None:
    """Render a static dashboard placeholder without data access."""
    with application_layout("Dashboard", "dashboard"):
        ui.label("Operational overview").classes("text-subtitle1 text-grey-7 mb-2")
        kpis = (
            ("QR Codes Generated Today", "—", "qr_code_2"),
            ("QR Labels Printed Today", "—", "print"),
            ("QR Reprints Today", "—", "replay"),
            ("Discarded QR Codes", "—", "delete_outline"),
            ("Active Devices", "—", "devices"),
            ("Inactive Devices", "—", "device_unknown"),
        )
        with ui.grid(columns="repeat(auto-fit, minmax(210px, 1fr))").classes("w-full gap-4"):
            for label, value, icon in kpis:
                with ui.card().classes("kpi-card p-5"):
                    with ui.row().classes("w-full items-start justify-between no-wrap"):
                        ui.label(label).classes("text-body2 text-grey-7")
                        ui.icon(icon).classes("text-primary text-2xl")
                    ui.label(value).classes("text-h4 text-weight-bold mt-3")

        with ui.card().classes("w-full mt-6 p-6"):
            ui.label("Recent activity").classes("text-h6 text-weight-medium")
            ui.separator().classes("my-3")
            ui.label("Live operational activity will appear after Supabase integration.").classes(
                "text-body2 text-grey-7"
            )
