def guard_int(a: Union[SymInt, int]) -> int:
    if isinstance(a, SymInt):
        return a.node.guard_int("", 0)  # NB: uses Python backtrace
    assert type(a) is int, a
    return a
