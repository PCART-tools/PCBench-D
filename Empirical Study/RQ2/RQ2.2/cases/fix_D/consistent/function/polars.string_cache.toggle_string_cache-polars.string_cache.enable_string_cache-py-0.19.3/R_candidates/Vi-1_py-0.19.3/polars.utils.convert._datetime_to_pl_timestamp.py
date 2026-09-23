def _datetime_to_pl_timestamp(dt: datetime, time_unit: TimeUnit | None) -> int:
    """Convert a python datetime to a timestamp in nanoseconds."""
    dt = dt.replace(tzinfo=timezone.utc) if dt.tzinfo != timezone.utc else dt
    if time_unit == "ns":
        micros = dt.microsecond
        return 1_000 * (_timestamp_in_seconds(dt) * 1_000_000 + micros)
    elif time_unit == "us" or time_unit is None:
        micros = dt.microsecond
        return _timestamp_in_seconds(dt) * 1_000_000 + micros
    elif time_unit == "ms":
        millis = dt.microsecond // 1000
        return _timestamp_in_seconds(dt) * 1_000 + millis
    else:
        raise ValueError(
            f"time_unit must be one of {{'ns', 'us', 'ms'}}, got {time_unit!r}"
        )
