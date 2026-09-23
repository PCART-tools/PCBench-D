def _mk_defaulter(d: T) -> Callable[[Optional[T]], T]:
    return lambda x: x if x is not None else d
