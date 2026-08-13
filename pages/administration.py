"""Administration pages."""

from nicegui import ui

from components.layout import placeholder_page
from services.printer_service import get_printer_status, print_test_labels


def render_users() -> None:
    """Render the user-management page."""
    placeholder_page(
        "Users",
        "users",
        "User management will be added with Supabase Auth.",
        "group",
    )


def render_devices() -> None:
    """Render the device-management page."""
    placeholder_page(
        "Devices",
        "devices",
        "Device management will be added after its approved data model is available.",
        "devices",
    )


def render_locations() -> None:
    """Render the location-management page."""
    placeholder_page(
        "Locations",
        "locations",
        "Location management will be added in a later administration stage.",
        "location_on",
    )


def render_printers() -> None:
    """Render printer administration."""

    with ui.column().classes("w-full gap-4"):

        ui.label("Printer Administration").classes(
            "text-h4 text-weight-bold"
        )

        ui.label(
            "Configure and test the QR label printer."
        ).classes("text-body2 text-grey-7")

        with ui.card().classes("w-full max-w-3xl p-6"):

            ui.label("Configured Printer").classes(
                "text-h6 text-weight-medium"
            )

            ui.separator().classes("my-3")

            status_label = ui.label(
                "Checking printer..."
            ).classes("text-body1")

            message_label = ui.label().classes(
                "text-body2 text-grey-7"
            )

            ui.button(
                "Test Connection",
                icon="refresh",
                on_click=lambda: check_printer(),
            ).props("no-caps")

            ui.separator().classes("my-4")

            ui.label("Test Print").classes(
                "text-h6 text-weight-medium"
            )

            ui.label(
                "Print one row containing two test QR labels."
            ).classes("text-body2 text-grey-7 mb-3")

            with ui.row().classes("w-full gap-4"):

                left_qr = ui.input(
                    "Left QR",
                    value="TEST001",
                ).props("outlined").classes("flex-1")

                right_qr = ui.input(
                    "Right QR",
                    value="TEST002",
                ).props("outlined").classes("flex-1")

            result_label = ui.label().classes(
                "text-body2 mt-3"
            )

            ui.button(
                "Print Test Labels",
                icon="print",
                on_click=lambda: test_print(),
            ).props("no-caps").classes("mt-3")

        def check_printer() -> None:
            status = get_printer_status()

            if status["connected"]:
                status_label.text = "Printer Connected"
                status_label.classes(
                    "text-positive",
                    remove="text-negative",
                )
            else:
                status_label.text = "? Printer Not Available"
                status_label.classes(
                    "text-negative",
                    remove="text-positive",
                )

            message_label.text = status["message"]

        def test_print() -> None:
            try:
                print_test_labels(
                    left_qr.value or "",
                    right_qr.value or "",
                )

                result_label.text = (
                    "Test print submitted successfully."
                )
                result_label.classes(
                    "text-positive",
                    remove="text-negative",
                )

            except Exception as exc:
                result_label.text = (
                    f"Print failed: {exc}"
                )
                result_label.classes(
                    "text-negative",
                    remove="text-positive",
                )

        check_printer()


def render_system_settings() -> None:
    """Render the global-settings page."""
    placeholder_page(
        "System Settings",
        "settings",
        "Global system settings will be added with role-based access control.",
        "settings",
    )


def render_audit_log() -> None:
    """Render the audit-log page."""
    placeholder_page(
        "Audit Log",
        "audit_log",
        "Audit data and filtering will be added in a later stage.",
        "fact_check",
    )
