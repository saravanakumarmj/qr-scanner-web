"""Administration pages."""

from nicegui import ui

from components.layout import placeholder_page, application_layout
from services.printer_service import get_printer_status, print_test_labels

from services.user_service import (
    create_user,
    list_users,
    update_user,
    set_user_active,
    reset_user_password,
)


def render_users() -> None:
    """Render the user-management page."""

    with application_layout("Users", "users"):

        ui.label(
            "Manage application users, roles, locations and access."
        ).classes("text-body2 text-grey-7 mb-4")

        table_container = ui.column().classes("w-full")

        def refresh_users() -> None:
            table_container.clear()

            users = list_users()

            with table_container:
                if not users:
                    ui.label(
                        "No users found."
                    ).classes("text-body2 text-grey-7")
                    return

                rows = [
                    {
                        "auth_user_id": user["auth_user_id"],
                        "user_id": user["user_id"],
                        "full_name": user["full_name"],
                        "role": user["role"],
                        "location": user.get("location") or "-",
                        "status": (
                            "Active"
                            if user["is_active"]
                            else "Inactive"
                        ),
                    }
                    for user in users
                ]

                columns = [
                    {
                        "name": "user_id",
                        "label": "User ID",
                        "field": "user_id",
                        "align": "left",
                    },
                    {
                        "name": "full_name",
                        "label": "Name",
                        "field": "full_name",
                        "align": "left",
                    },
                    {
                        "name": "role",
                        "label": "Role",
                        "field": "role",
                        "align": "left",
                    },
                    {
                        "name": "location",
                        "label": "Location",
                        "field": "location",
                        "align": "left",
                    },
                    {
                        "name": "status",
                        "label": "Status",
                        "field": "status",
                        "align": "left",
                    },
                    {
                        "name": "actions",
                        "label": "Actions",
                        "field": "actions",
                        "align": "right",
                    },
                ]

                table = ui.table(
                    columns=columns,
                    rows=rows,
                    row_key="auth_user_id",
                ).classes("w-full")

                table.add_slot(
                    "body-cell-actions",
                    r"""
                    <q-td :props="props">
                        <q-btn
                            flat
                            dense
                            round
                            icon="edit"
                            color="primary"
                            @click="$parent.$emit('edit', props.row)"
                        >
                            <q-tooltip>Edit User</q-tooltip>
                        </q-btn>

                        <q-btn
                            flat
                            dense
                            round
                            icon="lock_reset"
                            color="primary"
                            @click="$parent.$emit('password', props.row)"
                        >
                            <q-tooltip>Reset Password</q-tooltip>
                        </q-btn>

                        <q-btn
                            flat
                            dense
                            round
                            :icon="props.row.status === 'Active'
                                ? 'person_off'
                                : 'person'"
                            :color="props.row.status === 'Active'
                                ? 'negative'
                                : 'positive'"
                            @click="$parent.$emit('toggle', props.row)"
                        >
                            <q-tooltip>
                                {{ props.row.status === 'Active'
                                    ? 'Deactivate'
                                    : 'Activate' }}
                            </q-tooltip>
                        </q-btn>
                    </q-td>
                    """,
                )

                table.on("edit", lambda e: open_edit_dialog(e.args))
                table.on(
                    "password",
                    lambda e: open_password_dialog(e.args),
                )
                table.on(
                    "toggle",
                    lambda e: toggle_user(e.args),
                )

        def open_create_dialog() -> None:
            with ui.dialog() as dialog:
                with ui.card().classes("w-96 p-6"):

                    ui.label("Add User").classes(
                        "text-h6 text-weight-medium"
                    )

                    ui.separator().classes("my-3")

                    user_id = ui.input(
                        "User ID"
                    ).props("outlined").classes("w-full")

                    full_name = ui.input(
                        "Full Name"
                    ).props("outlined").classes("w-full mt-3")

                    password = ui.input(
                        "Password"
                    ).props(
                        "outlined type=password"
                    ).classes("w-full mt-3")

                    role = ui.select(
                        ["ADMIN", "OPERATOR", "VIEWER"],
                        value="OPERATOR",
                        label="Role",
                    ).props("outlined").classes("w-full mt-3")

                    location = ui.input(
                        "Location"
                    ).props("outlined").classes("w-full mt-3")

                    error = ui.label().classes(
                        "text-negative text-body2 mt-3"
                    )
                    error.visible = False

                    with ui.row().classes(
                        "w-full justify-end gap-2 mt-5"
                    ):

                        ui.button(
                            "Cancel",
                            on_click=dialog.close,
                        ).props("flat no-caps")

                        def save() -> None:
                            try:
                                create_user(
                                    user_id.value or "",
                                    password.value or "",
                                    full_name.value or "",
                                    role.value or "",
                                )

                                dialog.close()
                                refresh_users()

                                ui.notify(
                                    "User created successfully.",
                                    type="positive",
                                )

                            except Exception as exc:
                                error.text = str(exc)
                                error.visible = True

                        ui.button(
                            "Create User",
                            icon="person_add",
                            on_click=save,
                        ).props("no-caps")

            dialog.open()

        def open_edit_dialog(user: dict) -> None:
            with ui.dialog() as dialog:
                with ui.card().classes("w-96 p-6"):

                    ui.label("Edit User").classes(
                        "text-h6 text-weight-medium"
                    )

                    ui.separator().classes("my-3")

                    ui.input(
                        "User ID",
                        value=user["user_id"],
                    ).props(
                        "outlined readonly"
                    ).classes("w-full")

                    full_name = ui.input(
                        "Full Name",
                        value=user["full_name"],
                    ).props("outlined").classes("w-full mt-3")

                    role = ui.select(
                        ["ADMIN", "OPERATOR", "VIEWER"],
                        value=user["role"],
                        label="Role",
                    ).props("outlined").classes("w-full mt-3")

                    location = ui.input(
                        "Location",
                        value=user.get("location") or "",
                    ).props("outlined").classes("w-full mt-3")

                    error = ui.label().classes(
                        "text-negative text-body2 mt-3"
                    )
                    error.visible = False

                    with ui.row().classes(
                        "w-full justify-end gap-2 mt-5"
                    ):

                        ui.button(
                            "Cancel",
                            on_click=dialog.close,
                        ).props("flat no-caps")

                        def save() -> None:
                            try:
                                update_user(
                                    user["auth_user_id"],
                                    full_name.value or "",
                                    role.value or "",
                                    location.value,
                                )

                                dialog.close()
                                refresh_users()

                                ui.notify(
                                    "User updated successfully.",
                                    type="positive",
                                )

                            except Exception as exc:
                                error.text = str(exc)
                                error.visible = True

                        ui.button(
                            "Save",
                            icon="save",
                            on_click=save,
                        ).props("no-caps")

            dialog.open()

        def open_password_dialog(user: dict) -> None:
            with ui.dialog() as dialog:
                with ui.card().classes("w-96 p-6"):

                    ui.label("Reset Password").classes(
                        "text-h6 text-weight-medium"
                    )

                    ui.label(
                        f"User: {user['user_id']}"
                    ).classes("text-body2 text-grey-7 mt-2")

                    password = ui.input(
                        "New Password"
                    ).props(
                        "outlined type=password"
                    ).classes("w-full mt-4")

                    error = ui.label().classes(
                        "text-negative text-body2 mt-3"
                    )
                    error.visible = False

                    with ui.row().classes(
                        "w-full justify-end gap-2 mt-5"
                    ):

                        ui.button(
                            "Cancel",
                            on_click=dialog.close,
                        ).props("flat no-caps")

                        def save() -> None:
                            try:
                                reset_user_password(
                                    user["auth_user_id"],
                                    password.value or "",
                                )

                                dialog.close()

                                ui.notify(
                                    "Password reset successfully.",
                                    type="positive",
                                )

                            except Exception as exc:
                                error.text = str(exc)
                                error.visible = True

                        ui.button(
                            "Reset Password",
                            icon="lock_reset",
                            on_click=save,
                        ).props("no-caps")

            dialog.open()

        def toggle_user(user: dict) -> None:
            new_status = not (
                user["status"] == "Active"
            )

            action = (
                "activate"
                if new_status
                else "deactivate"
            )

            with ui.dialog() as dialog:
                with ui.card().classes("w-96 p-6"):

                    ui.label(
                        f"{action.title()} User"
                    ).classes(
                        "text-h6 text-weight-medium"
                    )

                    ui.label(
                        f"Are you sure you want to {action} "
                        f"'{user['user_id']}'?"
                    ).classes("text-body2 mt-3")

                    with ui.row().classes(
                        "w-full justify-end gap-2 mt-5"
                    ):

                        ui.button(
                            "Cancel",
                            on_click=dialog.close,
                        ).props("flat no-caps")

                        def confirm() -> None:
                            try:
                                set_user_active(
                                    user["auth_user_id"],
                                    new_status,
                                )

                                dialog.close()
                                refresh_users()

                                ui.notify(
                                    f"User {action}d successfully.",
                                    type="positive",
                                )

                            except Exception as exc:
                                ui.notify(
                                    str(exc),
                                    type="negative",
                                )

                        ui.button(
                            action.title(),
                            on_click=confirm,
                        ).props("no-caps")

            dialog.open()

        with ui.row().classes(
            "w-full justify-end mb-3"
        ):
            ui.button(
                "Add User",
                icon="person_add",
                on_click=open_create_dialog,
            ).props("no-caps")

        refresh_users()

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
