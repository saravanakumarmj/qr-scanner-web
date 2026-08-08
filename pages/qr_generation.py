"""QR generation page placeholder."""

from components.layout import placeholder_page


def render_qr_generation() -> None:
    """Render the deferred QR generation page."""
    placeholder_page(
        title="Generate QR",
        nav_key="generate",
        description="QR generation, sequence reservation, preview, and printing will be added in a later stage.",
        icon="qr_code_2",
    )
