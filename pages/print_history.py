"""Print history page placeholder."""

from components.layout import placeholder_page


def render_print_history() -> None:
    """Render the deferred print history page."""
    placeholder_page(
        title="Print History",
        nav_key="print_history",
        description="Print job history and filtering will be added with the print-history data model.",
        icon="history",
    )
