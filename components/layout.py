"""Shared page framing and placeholder presentation."""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager

from nicegui import ui

from components.footer import render_footer
from components.header import render_header
from components.navigation import render_navigation


@contextmanager
def application_layout(title: str, active_key: str) -> Iterator[None]:
    """Provide the common authenticated application shell for a page."""
    ui.colors(primary="#0d47a1", secondary="#00695c", accent="#ef6c00")
    ui.add_css(
        """
        body { background: #f3f6fa; }
        .q-page-container { background: #f3f6fa; }
        .app-content { max-width: 1500px; margin: 0 auto; }
        .kpi-card { min-height: 138px; border-left: 4px solid #0d47a1; }
        .placeholder-card { min-height: 250px; }
        .nav-entry { min-height: 42px; }
        """
    )
    with ui.header(elevated=True).classes("bg-primary text-white"):
        render_header()
    with ui.left_drawer(value=True).classes("bg-blue-grey-10 text-white"):
        render_navigation(active_key)
    with ui.footer().classes("bg-blue-grey-9 text-blue-grey-1"):
        render_footer()
    with ui.column().classes("app-content w-full p-6"):
        ui.label(title).classes("text-h4 text-weight-bold text-blue-grey-10")
        yield


def placeholder_page(title: str, nav_key: str, description: str, icon: str) -> None:
    """Render a consistent, non-functional page placeholder."""
    with application_layout(title, nav_key):
        with ui.card().classes("placeholder-card w-full p-8 flex flex-center"):
            with ui.column().classes("items-center text-center max-w-xl gap-3"):
                ui.icon(icon).classes("text-primary text-6xl")
                ui.label(title).classes("text-h5 text-weight-bold")
                ui.label("Planned module").classes("text-overline text-secondary")
                ui.label(description).classes("text-body1 text-grey-7")
