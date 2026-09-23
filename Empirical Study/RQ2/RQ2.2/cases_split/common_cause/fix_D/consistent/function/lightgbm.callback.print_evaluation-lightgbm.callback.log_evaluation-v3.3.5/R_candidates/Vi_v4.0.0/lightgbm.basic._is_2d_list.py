def _is_2d_list(data: Any) -> bool:
    """Check whether data is a 2-D list."""
    return isinstance(data, list) and len(data) > 0 and _is_1d_list(data[0])
