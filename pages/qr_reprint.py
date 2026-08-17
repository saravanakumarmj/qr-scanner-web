"""QR reprint page."""

from nicegui import ui

from components.layout import application_layout
from database.supabase_db import get_supabase_client
from services.printer_service import (
    get_printer_status,
    print_qr_batch,
)


def render_qr_reprint() -> None:
    """Render the QR bulk reprint page."""

    selected_ranges: list[dict] = []

    with application_layout("Reprint QR", "reprint"):

        ui.label("Reprint QR").classes(
            "text-h4 text-weight-bold"
        )

        ui.label(
            "Select one or more QR ranges and print them together."
        ).classes("text-body2 text-grey-7 mb-4")

        # ---------------------------------------------------------
        # Range selection
        # ---------------------------------------------------------

        with ui.card().classes("w-full p-5"):

            ui.label("Add QR Range").classes(
                "text-h6 text-weight-medium"
            )

            with ui.row().classes("w-full items-end gap-4"):

                start_qr = ui.input(
                    "Start QR",
                    placeholder="2608170001",
                ).props("outlined").classes("flex-1")

                end_qr = ui.input(
                    "End QR",
                    placeholder="2608170010",
                ).props("outlined").classes("flex-1")

                add_button = ui.button(
                    "Add Range",
                    icon="add",
                ).props("no-caps")

            error_label = ui.label().classes(
                "text-negative text-body2 mt-2"
            )
            error_label.visible = False

        # ---------------------------------------------------------
        # Selected ranges
        # ---------------------------------------------------------

        with ui.card().classes("w-full p-5 mt-4"):

            with ui.row().classes(
                "w-full items-center justify-between"
            ):
                ui.label("Selected Ranges").classes(
                    "text-h6 text-weight-medium"
                )

                total_label = ui.label(
                    "Total Labels: 0"
                ).classes("text-body1 text-weight-medium")

            ui.separator().classes("my-3")

            ranges_container = ui.column().classes("w-full gap-2")

            empty_label = ui.label(
                "No ranges selected."
            ).classes("text-body2 text-grey-7")

            # -----------------------------------------------------
            # Print section
            # -----------------------------------------------------

            ui.separator().classes("my-4")

            with ui.row().classes(
                "w-full justify-end items-center gap-4"
            ):

                print_status = ui.label().classes(
                    "text-body2"
                )

                print_button = ui.button(
                    "Print Selected",
                    icon="print",
                ).props(
                    "no-caps"
                )

        def refresh_ranges() -> None:
            """Refresh selected range display."""

            ranges_container.clear()

            total = sum(
                item["quantity"]
                for item in selected_ranges
            )

            total_label.text = f"Total Labels: {total}"

            empty_label.visible = not selected_ranges

            with ranges_container:
                for index, item in enumerate(selected_ranges):

                    with ui.row().classes(
                        "w-full items-center justify-between "
                        "border rounded p-3"
                    ):
                        with ui.row().classes(
                            "items-center gap-4"
                        ):
                            ui.label(
                                f"{item['start']} → {item['end']}"
                            ).classes(
                                "text-body1 text-weight-medium"
                            )

                            ui.label(
                                f"{item['quantity']} labels"
                            ).classes(
                                "text-body2 text-grey-7"
                            )

                        ui.button(
                            icon="delete",
                            on_click=lambda i=index: remove_range(i),
                        ).props(
                            "flat round dense color=negative"
                        )

        def ranges_overlap(
            start: int,
            end: int,
        ) -> bool:
            """Return True when the new range overlaps an existing range."""

            for item in selected_ranges:
                if not (
                    end < item["start_num"]
                    or start > item["end_num"]
                ):
                    return True

            return False

        def get_qr_range(
            start_qr_value: str,
            end_qr_value: str,
        ) -> list[dict]:
            """Get QR master records for a requested range."""

            client = get_supabase_client()

            response = (
                client.table("qr_master")
                .select("qr_code,qr_code_encoded")
                .gte("qr_code", start_qr_value)
                .lte("qr_code", end_qr_value)
                .order("qr_code")
                .execute()
            )

            return response.data or []

        def add_range() -> None:
            error_label.visible = False
            print_status.text = ""

            start = (start_qr.value or "").strip()
            end = (end_qr.value or "").strip()

            if not start or not end:
                error_label.text = (
                    "Start QR and End QR are required."
                )
                error_label.visible = True
                return

            if (
                len(start) != 10
                or len(end) != 10
                or not start.isdigit()
                or not end.isdigit()
            ):
                error_label.text = (
                    "QR code must be in YYMMDDNNNN format."
                )
                error_label.visible = True
                return

            start_num = int(start)
            end_num = int(end)

            if start_num > end_num:
                error_label.text = (
                    "Start QR must not be greater than End QR."
                )
                error_label.visible = True
                return

            # Keep ranges within the same date.
            if start[:6] != end[:6]:
                error_label.text = (
                    "Start and End QR must belong to the same date."
                )
                error_label.visible = True
                return

            if ranges_overlap(start_num, end_num):
                error_label.text = (
                    "This range overlaps an already selected range."
                )
                error_label.visible = True
                return

            try:
                rows = get_qr_range(start, end)

                expected_quantity = end_num - start_num + 1

                if len(rows) != expected_quantity:
                    error_label.text = (
                        "One or more QR codes in this range "
                        "do not exist."
                    )
                    error_label.visible = True
                    return

                selected_ranges.append(
                    {
                        "start": start,
                        "end": end,
                        "start_num": start_num,
                        "end_num": end_num,
                        "quantity": expected_quantity,
                        "rows": rows,
                    }
                )

                start_qr.value = ""
                end_qr.value = ""

                refresh_ranges()

            except Exception as exc:
                error_label.text = (
                    f"Unable to validate QR range: {exc}"
                )
                error_label.visible = True

        def remove_range(index: int) -> None:
            if 0 <= index < len(selected_ranges):
                selected_ranges.pop(index)

            refresh_ranges()

        def print_selected() -> None:
            print_status.text = ""

            if not selected_ranges:
                print_status.text = (
                    "Please add at least one QR range."
                )
                print_status.classes(
                    "text-negative",
                    remove="text-positive",
                )
                return

            try:
                encoded_values: list[str] = []

                for selected in selected_ranges:
                    for row in selected["rows"]:
                        encoded_values.append(
                            row["qr_code_encoded"]
                        )
                
                printer_status = get_printer_status()

                if not printer_status["connected"]:
                    print_status.text = (
                        "Printer not connected. "
                        "Please connect the printer and try again."
                    )
                    print_status.classes(
                        "text-negative",
                        remove="text-positive",
                    )
                    return
                    print_status.classes(
                        "text-negative",
                        remove="text-positive",
                    )
                    return

                
                rows_printed = print_qr_batch(
                    encoded_values
                )

                total = len(encoded_values)

                print_status.text = (
                    f"Print submitted successfully: "
                    f"{total} labels in {rows_printed} rows."
                )

                print_status.classes(
                    "text-positive",
                    remove="text-negative",
                )

                ui.notify(
                    "QR print submitted successfully.",
                    type="positive",
                )

            except Exception as exc:
                print_status.text = (
                    f"Print failed: {exc}"
                )
                print_status.classes(
                    "text-negative",
                    remove="text-positive",
                )

                ui.notify(
                    "QR printing failed.",
                    type="negative",
                )

        add_button.on_click(add_range)
        print_button.on_click(print_selected)

        refresh_ranges()