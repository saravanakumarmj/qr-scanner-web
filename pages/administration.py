"""Administration page placeholders."""

from components.layout import placeholder_page


def render_users() -> None:
    """Render the deferred user-management page."""
    placeholder_page("Users", "users", "User management will be added with Supabase Auth.", "group")


def render_devices() -> None:
    """Render the deferred device-management page."""
    placeholder_page("Devices", "devices", "Device management will be added after its approved data model is available.", "devices")


def render_locations() -> None:
    """Render the deferred location-management page."""
    placeholder_page("Locations", "locations", "Location management will be added in a later administration stage.", "location_on")


def render_printers() -> None:
    """Render the deferred printer-management page."""
    placeholder_page("Printers", "printers", "Printer management will be added with the printer service.", "print")


def render_system_settings() -> None:
    """Render the deferred global-settings page."""
    placeholder_page("System Settings", "settings", "Global system settings will be added with role-based access control.", "settings")


def render_audit_log() -> None:
    """Render the deferred audit-log page."""
    placeholder_page("Audit Log", "audit_log", "Audit data and filtering will be added in a later stage.", "fact_check")
