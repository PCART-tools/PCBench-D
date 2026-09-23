def _is_1d_list(data: Any) -> bool:
    """Check whether data is a 1-D list."""
    return isinstance(data, list) and (not data or _is_numeric(data[0]))
