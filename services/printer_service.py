"""Printer service for local Zebra printing."""

from __future__ import annotations

import win32print

from config import settings
from utils.zpl import build_two_label_zpl


class PrinterError(Exception):
    """Raised when a printer operation fails."""


def get_printer_name() -> str:
    """Return the configured printer name."""
    return settings.printer_name


def get_printer_status() -> dict:
    """Return the current status of the configured Windows printer."""

    if not settings.printer_enabled:
        return {
            "connected": False,
            "status": "DISABLED",
            "message": "Printer is disabled in configuration.",
        }

    try:
        printer = win32print.OpenPrinter(settings.printer_name)

        try:
            info = win32print.GetPrinter(printer, 2)
        finally:
            win32print.ClosePrinter(printer)

        status = info.get("Status", 0)

        return {
            "connected": True,
            "status": status,
            "message": "Printer is available.",
        }

    except Exception as exc:
        return {
            "connected": False,
            "status": "ERROR",
            "message": str(exc),
        }


def print_zpl(zpl: str) -> None:
    """Send raw ZPL to the configured Windows printer."""

    if not settings.printer_enabled:
        raise PrinterError("Printer is disabled.")

    if not zpl or not zpl.strip():
        raise PrinterError("ZPL data is empty.")

    try:
        printer = win32print.OpenPrinter(settings.printer_name)

        try:
            win32print.StartDocPrinter(
                printer,
                1,
                ("QR Management System", None, "RAW"),
            )

            try:
                win32print.StartPagePrinter(printer)

                try:
                    win32print.WritePrinter(
                        printer,
                        zpl.encode("utf-8"),
                    )
                finally:
                    win32print.EndPagePrinter(printer)

            finally:
                win32print.EndDocPrinter(printer)

        finally:
            win32print.ClosePrinter(printer)

    except Exception as exc:
        raise PrinterError(
            f"Unable to print to '{settings.printer_name}': {exc}"
        ) from exc


def print_test_labels(
    left_qr: str,
    right_qr: str | None = None,
) -> None:
    """Print one two-label test row."""

    zpl = build_two_label_zpl(
        left_qr,
        right_qr,
    )

    print_zpl(zpl)


def print_qr_batch(encoded_qr_values: list[str]) -> int:
    """Print a QR batch using two labels per physical row.

    Returns the number of physical print rows submitted.
    """

    if not encoded_qr_values:
        raise PrinterError("No QR codes available for printing.")

    rows_printed = 0

    for index in range(0, len(encoded_qr_values), 2):
        left_qr = encoded_qr_values[index]

        right_qr = (
            encoded_qr_values[index + 1]
            if index + 1 < len(encoded_qr_values)
            else None
        )

        zpl = build_two_label_zpl(
            left_qr,
            right_qr,
        )

        print_zpl(zpl)
        rows_printed += 1

    return rows_printed