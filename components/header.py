"""Shared application header."""

from nicegui import app, ui

from services.auth_service import logout


def render_header() -> None:
    """Render the authenticated application header."""

    user = app.storage.user.get("user", {})

    full_name = user.get("full_name", "User")
    role = user.get("role", "")

    with ui.row().classes("w-full items-center no-wrap px-4"):
        ui.label("Classic Pet ").classes(
            "text-h6 text-weight-bold"
        )

        ui.space()

        ui.icon("account_circle").classes("text-2xl")

        ui.label(full_name).classes("text-body2 ml-1")

        if role:
            ui.label(f"({role})").classes(
                "text-caption ml-1"
            )

        ui.button(
            "Logout",
            icon="logout",
            on_click=handle_logout,
        ).props(
            "outline no-caps"
        ).classes(
            "ml-3 text-white"
        )


def handle_logout() -> None:
    """Log out the current user and return to login."""

    logout()
    app.storage.user.clear()
    ui.navigate.to("/login")
