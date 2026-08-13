
"""Login page."""

from nicegui import ui, app

from services.auth_service import login
from services.auth_service import is_authenticated


def render_login() -> None:
    """Render the application login page."""

    ui.add_css("""
        body {
            background: #f3f6fa;
        }
    """)

    with ui.column().classes("absolute-center items-center gap-5"):
        with ui.card().classes("w-96 p-8 shadow-4"):
            ui.icon("qr_code_2").classes("text-5xl text-primary")

            ui.label("Can Management System").classes(
                "text-h5 text-weight-bold"
            )

            ui.label("Sign in to continue").classes(
                "text-body2 text-grey-7"
            )

            error_label = ui.label().classes(
                "text-negative text-body2"
            )
            error_label.visible = False

            user_id = ui.input(
                label="User ID",
                placeholder="Enter your User ID",
            ).props("outlined").classes("w-full")

            password = ui.input(
                label="Password",
                placeholder="Enter your password",
                password=True,
                password_toggle_button=True,
            ).props("outlined").classes("w-full")

            def handle_login() -> None:
                error_label.visible = False

                try:
                    user = login(
                        user_id.value or "",
                        password.value or "",
                    )

                    # Store the authenticated application user
                    # for the current NiceGUI client.
                    app.storage.user["user"] = {
                        "auth_user_id": user.auth_user_id,
                        "user_id": user.user_id,
                        "full_name": user.full_name,
                        "role": user.role,
                    }

                    ui.navigate.to("/dashboard")

                except ValueError as exc:
                    error_label.text = str(exc)
                    error_label.visible = True

                except Exception:
                    error_label.text = (
                        "Unable to sign in. Please try again."
                    )
                    error_label.visible = True

            login_button = ui.button(
                "Login",
                icon="login",
                on_click=handle_login,
            ).props("no-caps").classes("w-full")

            # Handle Enter from either input.
            ui.add_head_html("""
                <script>
                document.addEventListener('keydown', function(event) {
                    if (event.key !== 'Enter') {
                        return;
                    }

                    const active = document.activeElement;

                    if (
                        active &&
                        (
                            active.tagName === 'INPUT' ||
                            active.tagName === 'TEXTAREA'
                        )
                    ) {
                        event.preventDefault();

                        const buttons = Array.from(
                            document.querySelectorAll('button')
                        );

                        const loginButton = buttons.find(
                            button =>
                                button.innerText.trim() === 'Login'
                        );

                        if (loginButton) {
                            loginButton.click();
                        }
                    }
                });
                </script>
            """)


