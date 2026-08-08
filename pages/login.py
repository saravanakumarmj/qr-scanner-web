"""Login placeholder; Supabase Auth is intentionally deferred."""

from nicegui import ui


def render_login() -> None:
    """Render the unauthenticated shell placeholder."""
    ui.add_css("body { background: #f3f6fa; }")
    with ui.column().classes("absolute-center items-center gap-5"):
        with ui.card().classes("w-96 p-8 shadow-4"):
            ui.icon("qr_code_2").classes("text-5xl text-primary")
            ui.label("QR Management System").classes("text-h5 text-weight-bold")
            ui.label("Authentication will be added in a later stage.").classes(
                "text-body2 text-grey-7"
            )
            ui.button("Return to dashboard", on_click=lambda: ui.navigate.to("/dashboard")).props(
                "no-caps"
            ).classes("w-full")
