"""QR generation page."""

from nicegui import app, ui
from services.printer_service import check_print_agent


from components.layout import application_layout
from services.qr_service import (
    generate_qr_batch,
    print_qr_generation,
)


def render_qr_generation() -> None:
    """Render the QR generation page."""

    with application_layout("Generate QR", "generate"):

        ui.label(
            "Generate a new batch of QR codes."
        ).classes("text-subtitle1 text-grey-7 mb-4")

        with ui.card().classes("w-full max-w-2xl p-6"):

            ui.label("QR Generation").classes(
                "text-h6 text-weight-medium"
            )

            ui.label(
                "Enter the number of QR codes to generate."
            ).classes("text-body2 text-grey-7 mb-4")

            quantity = ui.number(
                label="Quantity",
                min=1,
                max=9999,
                value=1,
                step=1,
            ).props("outlined").classes("w-full")

            error_label = ui.label().classes(
                "text-negative text-body2 mt-3"
            )

            error_label.visible = False

            async def handle_generate() -> None:

                error_label.visible = False

                try:
                    requested_quantity = int(
                        quantity.value or 0
                    )

                    if requested_quantity <= 0:
                        raise ValueError(
                            "Quantity must be greater than zero."
                        )

                    if requested_quantity > 9999:
                        raise ValueError(
                            "Maximum QR generation quantity is 9999."
                        )

                    user = app.storage.user.get("user")

                    if not user:
                        ui.navigate.to("/login")
                        return

                    generated_by = user.get("user_id")

                    if not generated_by:
                        raise ValueError(
                            "Authenticated user information "
                            "is unavailable."
                        )


                    client = ui.context.client

                    printer_status = await check_print_agent(client)

                    if not printer_status["connected"]:
                        raise ValueError(
                            printer_status["message"]
                        )

                    result = generate_qr_batch(
                        requested_quantity,
                        generated_by,
                    )

                    with ui.dialog() as dialog:

                        with ui.card().classes("w-96 p-6"):

                            ui.label(
                                "Generation Summary"
                            ).classes(
                                "text-h6 text-weight-medium"
                            )

                            ui.separator().classes("my-3")

                            with ui.grid(columns="2").classes(
                                "w-full gap-y-3"
                            ):

                                ui.label("Quantity").classes(
                                    "text-grey-7"
                                )
                                ui.label(
                                    str(result.quantity)
                                )

                                ui.label(
                                    "Start QR Code"
                                ).classes("text-grey-7")
                                ui.label(
                                    result.start_qr_code
                                )

                                ui.label(
                                    "End QR Code"
                                ).classes("text-grey-7")
                                ui.label(
                                    result.end_qr_code
                                )

                                ui.label(
                                    "Print Status"
                                ).classes("text-grey-7")

                                status_label = ui.label(
                                    result.print_status
                                )

                            message_label = ui.label().classes(
                                "text-body2 mt-4"
                            )

                            with ui.row().classes(
                                "w-full justify-end gap-2 mt-5"
                            ):

                                print_button = ui.button(
                                    "Print QR Codes",
                                    icon="print",
                                ).props("no-caps")

                                ok_button = ui.button(
                                    "OK",
                                    on_click=dialog.close,
                                ).props("no-caps")

                                ok_button.visible = False

                            async def handle_print() -> None:

                                print_button.disable()

                                try:
                                    user = (
                                        app.storage.user.get("user")
                                    )

                                    if not user:
                                        ui.navigate.to("/login")
                                        return

                                    updated_by = user.get(
                                        "user_id"
                                    )

                                    if not updated_by:
                                        raise ValueError(
                                            "Authenticated user "
                                            "information is unavailable."
                                        )

                                    printed_quantity = (
                                        await print_qr_generation(
                                            generation_id=(
                                                result.generation_id
                                            ),
                                            start_qr_code=(
                                                result.start_qr_code
                                            ),
                                            end_qr_code=(
                                                result.end_qr_code
                                            ),
                                            updated_by=updated_by,
                                        )
                                    )

                                    status_label.text = "PRINTED"

                                    message_label.text = (
                                        f"{printed_quantity} QR codes "
                                        "submitted to the printer."
                                    )

                                    message_label.classes(
                                        "text-positive",
                                        remove="text-negative",
                                    )

                                    print_button.visible = False
                                    ok_button.visible = True

                                except Exception as exc:

                                    message_label.text = (
                                        f"Print failed: {exc}"
                                    )

                                    message_label.classes(
                                        "text-negative",
                                        remove="text-positive",
                                    )

                                    print_button.enable()

                            print_button.on_click(
                                handle_print
                            )

                    dialog.open()

                except ValueError as exc:

                    error_label.text = str(exc)
                    error_label.visible = True

                except Exception as exc:

                    error_label.text = (
                        f"Unable to generate QR codes: {exc}"
                    )
                    error_label.visible = True

            ui.button(
                "Generate QR Codes",
                icon="qr_code_2",
                on_click=handle_generate,
            ).props("no-caps").classes("w-full mt-4")