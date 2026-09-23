@lru_cache(64)
def is_namedtuple(cls: Any, *, annotated: bool = False) -> bool:
    """Check whether given class derives from NamedTuple."""
    if all(hasattr(cls, attr) for attr in ("_fields", "_field_defaults", "_replace")):
        if not isinstance(cls._fields, property):
            if not annotated or len(cls.__annotations__) == len(cls._fields):
                return all(isinstance(fld, str) for fld in cls._fields)
    return False
