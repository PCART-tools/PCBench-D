def _unpack_multi_column_dict(
    d: dict[str | Sequence[str], Any] | Any
) -> dict[str, Any] | Any:
    """Unpack multi-col dictionary into equivalent single-col definitions."""
    if not isinstance(d, dict):
        return d
    unpacked: dict[str, Any] = {}
    for key, value in d.items():
        if isinstance(key, str) or not isinstance(key, Sequence):
            key = (key,)
        for k in key:
            unpacked[k] = value
    return unpacked
