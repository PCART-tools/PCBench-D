def not_none(obj: Optional[T]) -> T:
    if obj is None:
        raise TypeError("Invariant encountered: value was None when it should not be")
    return obj
