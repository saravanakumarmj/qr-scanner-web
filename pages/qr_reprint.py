"""QR reprint page placeholder."""

from components.layout import placeholder_page


def render_qr_reprint() -> None:
    """Render the deferred QR reprint page."""
    placeholder_page(
        title="Reprint QR",
        nav_key="reprint",
        description="Search and reprint workflow is intentionally deferred until the print service is available.",
        icon="replay",
    )
