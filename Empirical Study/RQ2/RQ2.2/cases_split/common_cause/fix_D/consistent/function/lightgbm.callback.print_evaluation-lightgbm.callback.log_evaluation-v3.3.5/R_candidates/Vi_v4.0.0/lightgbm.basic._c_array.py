def _c_array(ctype: type, values: List[Any]) -> ctypes.Array:
    """Convert a Python array to C array."""
    return (ctype * len(values))(*values)  # type: ignore[operator]
