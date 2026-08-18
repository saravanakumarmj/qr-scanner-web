"""Application entry point for the QR Management System shell."""

from __future__ import annotations
from services.auth_service import is_authenticated

import logging
import os

from nicegui import ui, app

from config import settings
from database.supabase_db import get_supabase_status
from pages.administration import (
    render_audit_log,
    render_devices,
    render_locations,
    render_printers,
    render_system_settings,
    render_users,
)
from pages.dashboard import render_dashboard
from pages.login import render_login
from pages.print_history import render_print_history
from pages.profile import render_profile
from pages.qr_discard import render_qr_discard
from pages.qr_generation import render_qr_generation
from pages.qr_reprint import render_qr_reprint
from pages.reports import render_reports


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)


def log_supabase_startup_status() -> None:
    """Log the sanitized Supabase status before serving the application."""
    status = get_supabase_status(force_refresh=True)
    logger.info("Supabase startup status: %s", status.state.value)


@ui.page("/")
def index() -> None:
    """Route the root URL to the dashboard."""
    ui.navigate.to("/login")

def require_auth() -> bool:
    """Redirect unauthenticated clients to the login page."""
    if is_authenticated():
        return True

    ui.navigate.to("/login")
    return False


@ui.page("/login")
def login_page() -> None:
    render_login()


@ui.page("/dashboard")
def dashboard_page() -> None:
    if not require_auth():
        return
    render_dashboard()


@ui.page("/operations/generate")
def qr_generation_page() -> None:
    if not require_auth():
        return
    render_qr_generation()


@ui.page("/operations/reprint")
def qr_reprint_page() -> None:
    if not require_auth():
        return
    render_qr_reprint()


@ui.page("/operations/discard")
def qr_discard_page() -> None:
    if not require_auth():
        return
    render_qr_discard()


@ui.page("/operations/print-history")
def print_history_page() -> None:
    if not require_auth():
        return
    render_print_history()


@ui.page("/reports")
def reports_page() -> None:
    if not require_auth():
        return
    render_reports()


@ui.page("/administration/users")
def users_page() -> None:
    if not require_auth():
        return
    render_users()


@ui.page("/administration/devices")
def devices_page() -> None:
    if not require_auth():
        return
    render_devices()


@ui.page("/administration/locations")
def locations_page() -> None:
    if not require_auth():
        return
    render_locations()


@ui.page("/administration/printers")
def printers_page() -> None:
    if not require_auth():
        return
    render_printers()


@ui.page("/administration/settings")
def system_settings_page() -> None:
    if not require_auth():
        return
    render_system_settings()


@ui.page("/administration/audit-log")
def audit_log_page() -> None:
    if not require_auth():
        return
    render_audit_log()


@ui.page("/profile")
def profile_page() -> None:
    if not require_auth():
        return
    render_profile()


if __name__ in {"__main__", "__mp_main__"}:
    logger.info("Starting QR Management System application shell")
    log_supabase_startup_status()

    is_cloud_run = "PORT" in os.environ

    ui.run(
        host="0.0.0.0" if is_cloud_run else settings.app_host,
        port=int(os.environ.get("PORT", settings.app_port)),
        title=settings.app_name,
        reload=False if is_cloud_run else settings.app_reload,
        storage_secret=settings.nicegui_storage_secret,
    )
