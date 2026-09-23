def _to_python_datetime(
    value: int | float,
    time_unit: TimeUnit | None = "ns",
    time_zone: str | None = None,
) -> datetime:
    """Convert polars int64 timestamp to Python datetime."""
    if not time_zone:
        if time_unit == "us":
            return EPOCH + timedelta(microseconds=value)
        elif time_unit == "ns":
            return EPOCH + timedelta(microseconds=value // 1000)
        elif time_unit == "ms":
            return EPOCH + timedelta(milliseconds=value)
        else:
            raise ValueError(
                f"time_unit must be one of {{'ns','us','ms'}}, got {time_unit!r}"
            )
    elif _ZONEINFO_AVAILABLE:
        if time_unit == "us":
            dt = EPOCH_UTC + timedelta(microseconds=value)
        elif time_unit == "ns":
            dt = EPOCH_UTC + timedelta(microseconds=value // 1000)
        elif time_unit == "ms":
            dt = EPOCH_UTC + timedelta(milliseconds=value)
        else:
            raise ValueError(
                f"time_unit must be one of {{'ns','us','ms'}}, got {time_unit!r}"
            )
        return _localize(dt, time_zone)
    else:
        raise ImportError(
            "install polars[timezone] to handle datetimes with time zone information"
        )
