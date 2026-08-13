"""Dashboard page."""

from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

from nicegui import ui

from components.layout import application_layout
from database.dashboard_db import (
    get_live_device_metrics,
    get_period_metrics,
    get_recent_activity,
)


LOCAL_TIMEZONE = ZoneInfo("Asia/Kolkata")


def render_dashboard() -> None:
    """Render the QR Management dashboard."""

    today = datetime.now(LOCAL_TIMEZONE).date()

    date_range = {
        "from": today,
        "to": today,
    }

    # ==============================================================
    # Helpers
    # ==============================================================

    def format_range() -> str:
        start = date_range["from"]
        end = date_range["to"]

        if start == end:
            return start.strftime("%d %b %Y")

        return (
            f"{start.strftime('%d %b %Y')} - "
            f"{end.strftime('%d %b %Y')}"
        )

    def set_value(label, value: int) -> None:
        label.set_text(f"{value:,}")

    # ==============================================================
    # Refresh
    # ==============================================================

    def refresh_period() -> None:
        """Refresh date-dependent dashboard data."""

        try:
            metrics = get_period_metrics(
                date_range["from"],
                date_range["to"],
            )

            set_value(qr_generated_value, metrics["qr_generated"])
            set_value(labels_printed_value, metrics["labels_printed"])

            set_value(success_value, metrics["success"])
            set_value(flagged_value, metrics["flagged"])
            set_value(discarded_value, metrics["discarded"])
            set_value(invalid_value, metrics["invalid"])
            set_value(error_value, metrics["error"])

            activities = get_recent_activity(
                date_range["from"],
                date_range["to"],
            )

            activity_table.rows = activities
            activity_table.update()

        except Exception as error:
            ui.notify(
                f"Unable to load dashboard data: {error}",
                type="negative",
            )

    def refresh_live() -> None:
        """Refresh current device status."""

        try:
            metrics = get_live_device_metrics()

            set_value(active_devices_value, metrics["active"])
            set_value(inactive_devices_value, metrics["inactive"])
            set_value(maintenance_value, metrics["maintenance"])

        except Exception as error:
            ui.notify(
                f"Unable to load live status: {error}",
                type="negative",
            )

    def refresh_dashboard() -> None:
        refresh_period()
        refresh_live()

    # ==============================================================
    # Date range
    # ==============================================================

    def set_range(
        start: date,
        end: date,
    ) -> None:

        if start > end:
            ui.notify(
                "From date cannot be after To date.",
                type="warning",
            )
            return

        date_range["from"] = start
        date_range["to"] = end

        date_range_label.set_text(format_range())

        refresh_period()

    # ==============================================================
    # Custom date dialog
    # ==============================================================

    with ui.dialog() as date_dialog:
        with ui.card().classes("p-4"):

            ui.label(
                "Custom Date Range"
            ).classes(
                "text-subtitle1 text-weight-medium"
            )

            with ui.row().classes(
                "items-center gap-3 mt-2"
            ):

                custom_from = ui.date(
                    value=today.isoformat()
                ).props("minimal")

                ui.label("to").classes(
                    "text-caption text-grey-7"
                )

                custom_to = ui.date(
                    value=today.isoformat()
                ).props("minimal")

            with ui.row().classes(
                "w-full justify-end gap-2 mt-3"
            ):

                ui.button(
                    "Cancel",
                    on_click=date_dialog.close,
                ).props("flat")

                def apply_custom_range() -> None:

                    start = date.fromisoformat(
                        custom_from.value
                    )

                    end = date.fromisoformat(
                        custom_to.value
                    )

                    set_range(start, end)

                    date_dialog.close()

                ui.button(
                    "Apply",
                    on_click=apply_custom_range,
                ).props("unelevated")

    # ==============================================================
    # Dashboard
    # ==============================================================

    with application_layout(
        "Dashboard",
        "dashboard",
    ):

        # ----------------------------------------------------------
        # Header
        # ----------------------------------------------------------

        with ui.row().classes(
            "w-full items-center justify-between mb-5"
        ):

            with ui.column().classes("gap-0"):

                ui.label(
                    "Production and operational overview"
                ).classes(
                    "text-h6 text-weight-medium"
                )


            with ui.row().classes(
                "items-center gap-1"
            ):

                date_range_label = ui.label(
                    format_range()
                ).classes(
                    "text-caption text-grey-7 mr-2"
                )

                ui.button(
                    "Today",
                    on_click=lambda: set_range(
                        today,
                        today,
                    ),
                ).props(
                    "outline dense"
                )

                ui.button(
                    "7 Days",
                    on_click=lambda: set_range(
                        today - timedelta(days=6),
                        today,
                    ),
                ).props(
                    "flat dense"
                )

                ui.button(
                    icon="calendar_month",
                    on_click=date_dialog.open,
                ).props(
                    "flat round dense"
                ).tooltip(
                    "Custom date range"
                )

                ui.button(
                    icon="refresh",
                    on_click=refresh_dashboard,
                ).props(
                    "flat round dense"
                ).tooltip(
                    "Refresh dashboard"
                )

        # ==========================================================
        # SELECTED PERIOD
        # ==========================================================

        with ui.card().classes(
            "w-full p-5"
        ):

            with ui.row().classes(
                "w-full items-center justify-between"
            ):

                with ui.column().classes("gap-0"):

                    ui.label(
                        "Selected Period"
                    ).classes(
                        "text-subtitle1 text-weight-medium"
                    )

                    ui.label(
                        "Production and scan activity"
                    ).classes(
                        "text-caption text-grey-7"
                    )

            # ------------------------------------------------------
            # Production
            # ------------------------------------------------------

            ui.label(
                "Production"
            ).classes(
                "text-caption text-grey-6 mt-4 mb-2"
            )

            with ui.grid(
                columns="repeat(2, minmax(0, 1fr))"
            ).classes(
                "w-full gap-3"
            ):

                with ui.card().classes(
                    "kpi-card p-4"
                ):
                    ui.label(
                        "QR Generated"
                    ).classes(
                        "text-caption text-grey-7"
                    )

                    qr_generated_value = ui.label(
                        "—"
                    ).classes(
                        "text-h5 text-weight-bold mt-1"
                    )

                with ui.card().classes(
                    "kpi-card p-4"
                ):
                    ui.label(
                        "Labels Printed"
                    ).classes(
                        "text-caption text-grey-7"
                    )

                    labels_printed_value = ui.label(
                        "—"
                    ).classes(
                        "text-h5 text-weight-bold mt-1"
                    )

            # ------------------------------------------------------
            # Scan Activity
            # ------------------------------------------------------

            ui.label(
                "Scan Activity"
            ).classes(
                "text-caption text-grey-6 mt-5 mb-2"
            )

            with ui.grid(
                columns="repeat(5, minmax(0, 1fr))"
            ).classes(
                "w-full gap-3"
            ):

                scan_cards = [
                    ("Success", "check_circle"),
                    ("Flagged", "flag"),
                    ("Discarded", "delete_outline"),
                    ("Invalid", "block"),
                    ("Error", "error_outline"),
                ]

                scan_values = {}

                for label, icon in scan_cards:

                    with ui.card().classes(
                        "kpi-card p-3"
                    ):

                        with ui.row().classes(
                            "items-center gap-2"
                        ):

                            ui.icon(icon).classes(
                                "text-lg"
                            )

                            ui.label(label).classes(
                                "text-caption text-grey-7"
                            )

                        scan_values[label] = ui.label(
                            "—"
                        ).classes(
                            "text-h6 text-weight-bold mt-1"
                        )

            success_value = scan_values["Success"]
            flagged_value = scan_values["Flagged"]
            discarded_value = scan_values["Discarded"]
            invalid_value = scan_values["Invalid"]
            error_value = scan_values["Error"]

        # ==========================================================
        # LIVE OPERATIONS
        # ==========================================================

        with ui.card().classes(
            "w-full mt-4 p-5"
        ):

            with ui.row().classes(
                "w-full items-center justify-between"
            ):

                with ui.column().classes("gap-0"):

                    ui.label(
                        "Live Operations"
                    ).classes(
                        "text-subtitle1 text-weight-medium"
                    )

                    ui.label(
                        "Current system and device status"
                    ).classes(
                        "text-caption text-grey-7"
                    )

                with ui.row().classes(
                    "items-center gap-1"
                ):

                    ui.icon(
                        "circle"
                    ).classes(
                        "text-green text-xs"
                    )

                    ui.label(
                        "LIVE"
                    ).classes(
                        "text-caption text-weight-medium"
                    )

            # ------------------------------------------------------
            # Device status
            # ------------------------------------------------------

            with ui.grid(
                columns="repeat(3, minmax(0, 1fr))"
            ).classes(
                "w-full gap-3 mt-4"
            ):

                with ui.card().classes(
                    "kpi-card p-4"
                ):
                    ui.label(
                        "Active Devices"
                    ).classes(
                        "text-caption text-grey-7"
                    )

                    active_devices_value = ui.label(
                        "—"
                    ).classes(
                        "text-h5 text-weight-bold mt-1"
                    )

                with ui.card().classes(
                    "kpi-card p-4"
                ):
                    ui.label(
                        "Inactive Devices"
                    ).classes(
                        "text-caption text-grey-7"
                    )

                    inactive_devices_value = ui.label(
                        "—"
                    ).classes(
                        "text-h5 text-weight-bold mt-1"
                    )

                with ui.card().classes(
                    "kpi-card p-4"
                ):
                    ui.label(
                        "Maintenance"
                    ).classes(
                        "text-caption text-grey-7"
                    )

                    maintenance_value = ui.label(
                        "—"
                    ).classes(
                        "text-h5 text-weight-bold mt-1"
                    )

        # ==========================================================
        # RECENT ACTIVITY
        # ==========================================================

        with ui.card().classes(
            "w-full mt-4 p-5"
        ):

            ui.label(
                "Recent Activity"
            ).classes(
                "text-subtitle1 text-weight-medium"
            )

            ui.label(
                "Latest scan transactions for the selected period"
            ).classes(
                "text-caption text-grey-7"
            )

            ui.separator().classes("my-3")

            activity_table = ui.table(
                columns=[
                    {
                        "name": "scan_ts",
                        "label": "Time",
                        "field": "scan_ts",
                    },
                    {
                        "name": "qr_code",
                        "label": "QR Code",
                        "field": "qr_code",
                    },
                    {
                        "name": "device_id",
                        "label": "Device",
                        "field": "device_id",
                    },
                    {
                        "name": "scan_result",
                        "label": "Result",
                        "field": "scan_result",
                    },
                    {
                        "name": "cycle_count",
                        "label": "Cycle",
                        "field": "cycle_count",
                    },
                ],
                rows=[],
                row_key="transaction_id",
            ).classes(
                "w-full"
            )

    # ==============================================================
    # Initial load
    # ==============================================================

    refresh_dashboard()