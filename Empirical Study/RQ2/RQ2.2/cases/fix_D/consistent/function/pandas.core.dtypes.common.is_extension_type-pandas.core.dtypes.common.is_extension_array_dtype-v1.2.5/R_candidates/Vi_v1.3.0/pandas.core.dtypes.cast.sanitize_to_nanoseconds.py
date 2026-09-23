def sanitize_to_nanoseconds(values: np.ndarray, copy: bool = False) -> np.ndarray:
    """
    Safely convert non-nanosecond datetime64 or timedelta64 values to nanosecond.
    """
    dtype = values.dtype
    if dtype.kind == "M" and dtype != DT64NS_DTYPE:
        values = conversion.ensure_datetime64ns(values)

    elif dtype.kind == "m" and dtype != TD64NS_DTYPE:
        values = conversion.ensure_timedelta64ns(values)

    elif copy:
        values = values.copy()

    return values
