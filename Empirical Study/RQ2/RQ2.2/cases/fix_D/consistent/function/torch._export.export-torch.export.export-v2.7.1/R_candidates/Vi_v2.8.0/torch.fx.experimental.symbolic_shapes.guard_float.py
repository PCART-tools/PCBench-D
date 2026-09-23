def guard_float(a: FloatLikeType) -> float:
    if isinstance(a, SymFloat):
        return a.node.guard_float("", 0)  # NB: uses Python backtrace
    assert isinstance(a, float), a
    return a
