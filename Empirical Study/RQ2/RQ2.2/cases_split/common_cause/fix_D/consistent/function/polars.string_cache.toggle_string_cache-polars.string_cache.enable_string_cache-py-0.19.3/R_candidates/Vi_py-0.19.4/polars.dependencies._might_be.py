@lru_cache(maxsize=None)
def _might_be(cls: type, type_: str) -> bool:
    # infer whether the given class "might" be associated with the given
    # module (in which case it's reasonable to do a real isinstance check)
    try:
        return any(f"{type_}." in str(o) for o in cls.mro())
    except TypeError:
        return False
