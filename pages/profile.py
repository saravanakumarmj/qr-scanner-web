"""Profile page placeholder."""

from components.layout import placeholder_page


def render_profile() -> None:
    """Render the deferred profile page."""
    placeholder_page(
        title="Profile",
        nav_key="profile",
        description="Authenticated user profile details will be available after Supabase Auth is implemented.",
        icon="account_circle",
    )
