"""Common printing service for the QR Management Web App."""

from __future__ import annotations

import json
from typing import Any

from nicegui import Client, ui

from config import settings
from utils.zpl import build_two_label_zpl


class PrinterError(Exception):
    """Raised when a printer operation fails."""


def get_printer_name() -> str:
    """Return the configured printer name."""
    return settings.printer_name or "Windows Print Agent"


def get_print_agent_url() -> str:
    """Return the local Windows Print Agent URL."""
    return settings.print_agent_url.rstrip("/")

def get_printer_status() -> dict[str, str | bool]:
    """Return configured print-agent status.

    The physical printer is checked by the Windows Print Agent.
    This function only reports whether printing is configured.
    """

    if not settings.printer_enabled:
        return {
            "connected": False,
            "status": "DISABLED",
            "message": "Printer is disabled in configuration.",
        }

    if not settings.print_agent_url:
        return {
            "connected": False,
            "status": "NOT_CONFIGURED",
            "message": "Print agent is not configured.",
        }

    return {
        "connected": True,
        "status": "AVAILABLE",
        "message": "Print agent configured.",
    }
    
def build_print_zpl(
    encoded_qr_values: list[str],
) -> str:
    """Build ZPL for a QR batch without printing it."""

    if not encoded_qr_values:
        raise PrinterError(
            "No QR codes available for printing."
        )

    zpl_parts: list[str] = []

    for index in range(0, len(encoded_qr_values), 2):
        left_qr = encoded_qr_values[index]

        right_qr = (
            encoded_qr_values[index + 1]
            if index + 1 < len(encoded_qr_values)
            else None
        )

        zpl_parts.append(
            build_two_label_zpl(
                left_qr,
                right_qr,
            )
        )

    return "".join(zpl_parts)


async def check_print_agent(
    client: Client,
) -> dict[str, Any]:
    """Check the local Windows Print Agent."""

    if not settings.printer_enabled:
        return {
            "connected": False,
            "status": "DISABLED",
            "message": "Printer is disabled.",
        }

    if not settings.print_agent_url:
        return {
            "connected": False,
            "status": "NOT_CONFIGURED",
            "message": "Print agent is not configured.",
        }

    agent_url = json.dumps(
        f"{get_print_agent_url()}/health"
    )

    result = await client.run_javascript(
        f"""
        (async () => {{
            try {{
                const response = await fetch(
                    {agent_url}
                );

                const data = await response.json();

                return {{
                    success: response.ok,
                    data: data
                }};
            }} catch (error) {{
                return {{
                    success: false,
                    data: {{
                        printer_available: false,
                        message: error.message
                    }}
                }};
            }}
        }})()
        """,
        timeout=5.0,
    )

    if not result or not result.get("success"):
        return {
            "connected": False,
            "status": "AGENT_OFFLINE",
            "message": (
                "Windows Print Agent is not available."
            ),
        }

    data = result.get("data", {})

    if data.get("printer_available"):
        return {
            "connected": True,
            "status": "READY",
            "message": "Printer is connected.",
        }

    return {
        "connected": False,
        "status": "OFFLINE",
        "message": "Printer is not connected.",
    }


async def print_zpl(
    client: Client,
    zpl: str,
) -> dict[str, Any]:
    """Send ZPL to the local Windows Print Agent."""

    if not settings.printer_enabled:
        raise PrinterError(
            "Printer is disabled."
        )

    if not settings.print_agent_url:
        raise PrinterError(
            "Print agent is not configured."
        )

    if not zpl or not zpl.strip():
        raise PrinterError(
            "ZPL data is empty."
        )

    agent_url = json.dumps(
        f"{get_print_agent_url()}/print"
    )

    zpl_value = json.dumps(zpl)

    result = await client.run_javascript(
        f"""
        (async () => {{
            try {{
                const response = await fetch(
                    {agent_url},
                    {{
                        method: "POST",
                        headers: {{
                            "Content-Type": "application/json"
                        }},
                        body: JSON.stringify({{
                            zpl: {zpl_value}
                        }})
                    }}
                );

                const data = await response.json();

                return {{
                    success:
                        response.ok &&
                        data.success === true,
                    data: data
                }};

            }} catch (error) {{
                return {{
                    success: false,
                    data: {{
                        detail: error.message
                    }}
                }};
            }}
        }})()
        """,
        timeout=15.0,
    )

    if not result:
        raise PrinterError(
            "No response received from the Print Agent."
        )

    if result.get("success"):
        return result.get("data", {})

    data = result.get("data", {})

    raise PrinterError(
        data.get(
            "detail",
            "Print request failed.",
        )
    )


async def print_qr_batch(
    client: Client,
    encoded_qr_values: list[str],
) -> int:
    """Print a QR batch through the Windows Print Agent."""

    if not encoded_qr_values:
        raise PrinterError(
            "No QR codes available for printing."
        )

    zpl = build_print_zpl(
        encoded_qr_values
    )

    await print_zpl(
        client,
        zpl,
    )

    return (
        len(encoded_qr_values) + 1
    ) // 2


async def print_test_labels(
    client: Client,
    left_qr: str,
    right_qr: str | None = None,
) -> None:
    """Print one two-label test row."""

    zpl = build_two_label_zpl(
        left_qr,
        right_qr,
    )

    await print_zpl(
        client,
        zpl,
    )