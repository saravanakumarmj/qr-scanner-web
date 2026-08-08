"""Reports page placeholder."""

from components.layout import placeholder_page


def render_reports() -> None:
    """Render the deferred reports page."""
    placeholder_page(
        title="Reports",
        nav_key="reports",
        description="Operational reports and CSV export will be added after the required data services exist.",
        icon="assessment",
    )
