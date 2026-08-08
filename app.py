"""Application entry point for the QR Management System shell."""

from __future__ import annotations

import logging

from nicegui import ui

from config import settings
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


@ui.page("/")
def index() -> None:
    """Route the root URL to the dashboard."""
    ui.navigate.to("/dashboard")


@ui.page("/login")
def login_page() -> None:
    render_login()


@ui.page("/dashboard")
def dashboard_page() -> None:
    render_dashboard()


@ui.page("/operations/generate")
def qr_generation_page() -> None:
    render_qr_generation()


@ui.page("/operations/reprint")
def qr_reprint_page() -> None:
    render_qr_reprint()


@ui.page("/operations/discard")
def qr_discard_page() -> None:
    render_qr_discard()


@ui.page("/operations/print-history")
def print_history_page() -> None:
    render_print_history()


@ui.page("/reports")
def reports_page() -> None:
    render_reports()


@ui.page("/administration/users")
def users_page() -> None:
    render_users()


@ui.page("/administration/devices")
def devices_page() -> None:
    render_devices()


@ui.page("/administration/locations")
def locations_page() -> None:
    render_locations()


@ui.page("/administration/printers")
def printers_page() -> None:
    render_printers()


@ui.page("/administration/settings")
def system_settings_page() -> None:
    render_system_settings()


@ui.page("/administration/audit-log")
def audit_log_page() -> None:
    render_audit_log()


@ui.page("/profile")
def profile_page() -> None:
    render_profile()


if __name__ in {"__main__", "__mp_main__"}:
    logger.info("Starting QR Management System application shell")
    ui.run(
        host=settings.app_host,
        port=settings.app_port,
        title=settings.app_name,
        reload=settings.app_reload,
    )
