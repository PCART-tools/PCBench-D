def arrlen(obj: Any) -> int | None:
    """Return length of (non-string) sequence object; returns None for non-sequences."""
    try:
        return None if isinstance(obj, str) else len(obj)
    except TypeError:
        return None
