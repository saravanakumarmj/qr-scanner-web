"""Dashboard data access."""

from __future__ import annotations

from datetime import date, datetime, time, timedelta
from typing import Any
from zoneinfo import ZoneInfo

from database.supabase_db import get_supabase_client


LOCAL_TIMEZONE = ZoneInfo("Asia/Kolkata")
UTC = ZoneInfo("UTC")


def _date_range_utc(
    from_date: date,
    to_date: date,
) -> tuple[str, str]:
    """Convert an inclusive India-local date range to UTC."""

    start_local = datetime.combine(
        from_date,
        time.min,
        tzinfo=LOCAL_TIMEZONE,
    )

    end_local = datetime.combine(
        to_date + timedelta(days=1),
        time.min,
        tzinfo=LOCAL_TIMEZONE,
    )

    return (
        start_local.astimezone(UTC).isoformat(),
        end_local.astimezone(UTC).isoformat(),
    )


def get_period_metrics(
    from_date: date,
    to_date: date,
) -> dict[str, int]:
    """Return production and scan metrics for the selected period."""

    start_ts, end_ts = _date_range_utc(
        from_date,
        to_date,
    )

    client = get_supabase_client()

    # --------------------------------------------------------------
    # Production
    # --------------------------------------------------------------
    generated = (
        client.table("qr_master")
        .select("qr_code", count="exact")
        .gte("created_ts", start_ts)
        .lt("created_ts", end_ts)
        .execute()
    )

    printed = (
        client.table("qr_master")
        .select("qr_code", count="exact")
        .not_.is_("qr_printed_ts", "null")
        .gte("qr_printed_ts", start_ts)
        .lt("qr_printed_ts", end_ts)
        .execute()
    )

    # --------------------------------------------------------------
    # Scan activity
    # --------------------------------------------------------------
    scan_result = (
        client.table("qr_transaction")
        .select("transaction_id, scan_result", count="exact")
        .gte("scan_ts", start_ts)
        .lt("scan_ts", end_ts)
        .execute()
    )

    transactions = scan_result.data or []

    scan_counts = {
        "SUCCESS": 0,
        "FLAGGED": 0,
        "DISCARDED": 0,
        "INVALID": 0,
        "ERROR": 0,
    }

    for transaction in transactions:
        result = transaction.get("scan_result")

        if result in scan_counts:
            scan_counts[result] += 1

    return {
        "qr_generated": generated.count or 0,
        "labels_printed": printed.count or 0,
        "success": scan_counts["SUCCESS"],
        "flagged": scan_counts["FLAGGED"],
        "discarded": scan_counts["DISCARDED"],
        "invalid": scan_counts["INVALID"],
        "error": scan_counts["ERROR"],
    }


def get_live_device_metrics() -> dict[str, int]:
    """Return current device status counts."""

    client = get_supabase_client()

    active = (
        client.table("qr_device")
        .select("device_id", count="exact")
        .eq("status", "ACTIVE")
        .execute()
    )

    inactive = (
        client.table("qr_device")
        .select("device_id", count="exact")
        .eq("status", "INACTIVE")
        .execute()
    )

    maintenance = (
        client.table("qr_device")
        .select("device_id", count="exact")
        .eq("status", "MAINTENANCE")
        .execute()
    )

    return {
        "active": active.count or 0,
        "inactive": inactive.count or 0,
        "maintenance": maintenance.count or 0,
    }


def get_recent_activity(
    from_date: date,
    to_date: date,
    limit: int = 10,
) -> list[dict[str, Any]]:
    """Return recent scan activity for the selected period."""

    start_ts, end_ts = _date_range_utc(
        from_date,
        to_date,
    )

    client = get_supabase_client()

    result = (
        client.table("qr_transaction")
        .select(
            """
            transaction_id,
            qr_code,
            device_id,
            scan_ts,
            cycle_count,
            scan_result,
            event_reason,
            result_code
            """
        )
        .gte("scan_ts", start_ts)
        .lt("scan_ts", end_ts)
        .order("scan_ts", desc=True)
        .limit(limit)
        .execute()
    )

    return result.data or []