def contains_nested(value: Any, is_nested: Callable[[Any], bool]) -> bool:
    """Determine if value contains (or is) nested structured data."""
    if is_nested(value):
        return True
    elif isinstance(value, dict):
        return any(contains_nested(v, is_nested) for v in value.values())
    elif isinstance(value, (list, tuple)):
        return any(contains_nested(v, is_nested) for v in value)
    return False
