def _warn_for_deprecated_date_range_use(
    start: date | datetime | IntoExpr,
    end: date | datetime | IntoExpr,
    interval: str,
    time_unit: TimeUnit | None,
    time_zone: str | None,
) -> None:
    # This check is not foolproof, but should catch most cases
    if (
        isinstance(start, datetime)
        or isinstance(end, datetime)
        or "s" in interval
        or "h" in interval
        or ("m" in interval and "mo" not in interval)
        or time_unit is not None
        or time_zone is not None
    ):
        issue_deprecation_warning(
            "Creating Datetime ranges using `date_range(s)` is deprecated."
            " Use `datetime_range(s)` instead.",
            version="0.19.3",
        )
