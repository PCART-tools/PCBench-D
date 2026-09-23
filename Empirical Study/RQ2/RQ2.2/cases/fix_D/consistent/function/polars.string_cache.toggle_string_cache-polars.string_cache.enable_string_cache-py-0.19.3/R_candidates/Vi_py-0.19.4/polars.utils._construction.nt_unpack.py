def nt_unpack(obj: Any) -> Any:
    """Recursively unpack a nested NamedTuple."""
    if isinstance(obj, dict):
        return {key: nt_unpack(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [nt_unpack(value) for value in obj]
    elif is_namedtuple(obj.__class__):
        return {key: nt_unpack(value) for key, value in obj._asdict().items()}
    elif isinstance(obj, tuple):
        return tuple(nt_unpack(value) for value in obj)
    else:
        return obj
