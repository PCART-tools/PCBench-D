def empty_list(value: Any, *, nested: bool) -> bool:
    """Check if value is an empty list, or a list that contains only empty lists."""
    if isinstance(value, list):
        return (
            True
            if value and not nested
            else all(empty_list(v, nested=True) for v in value)
        )
    return False
