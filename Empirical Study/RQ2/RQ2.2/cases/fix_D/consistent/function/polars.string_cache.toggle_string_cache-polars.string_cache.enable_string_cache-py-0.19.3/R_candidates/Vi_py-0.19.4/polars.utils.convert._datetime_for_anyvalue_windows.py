def _datetime_for_anyvalue_windows(dt: datetime) -> tuple[float, int]:
    """Used in pyo3 anyvalue conversion."""
    if dt.tzinfo is None:
        dt = _localize(dt, "UTC")
    # returns (s, ms)
    return (_timestamp_in_seconds(dt), dt.microsecond)
