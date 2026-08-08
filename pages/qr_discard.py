"""QR discard page placeholder."""

from components.layout import placeholder_page


def render_qr_discard() -> None:
    """Render the deferred QR discard page."""
    placeholder_page(
        title="Discard QR",
        nav_key="discard",
        description="Discard lifecycle support requires an approved database design and will be added later.",
        icon="delete_outline",
    )
