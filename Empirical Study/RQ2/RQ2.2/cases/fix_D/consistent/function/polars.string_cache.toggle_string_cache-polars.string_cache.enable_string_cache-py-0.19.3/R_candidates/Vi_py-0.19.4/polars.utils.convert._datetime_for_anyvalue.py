def _datetime_for_anyvalue(dt: datetime) -> tuple[int, int]:
    """Used in pyo3 anyvalue conversion."""
    # returns (s, ms)
    if dt.tzinfo is None:
        return (
            _timestamp_in_seconds(dt.replace(tzinfo=timezone.utc)),
            dt.microsecond,
        )
    return (_timestamp_in_seconds(dt), dt.microsecond)
