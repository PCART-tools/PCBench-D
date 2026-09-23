def is_int_sequence(val: object) -> TypeGuard[Sequence[int]]:
    """Check whether the given sequence is a sequence of integers."""
    return isinstance(val, Sequence) and _is_iterable_of(val, int)
