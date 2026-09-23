def is_bool_sequence(val: object) -> TypeGuard[Sequence[bool]]:
    """Check whether the given sequence is a sequence of booleans."""
    return isinstance(val, Sequence) and _is_iterable_of(val, bool)
