def guard_scalar(
    a: Union[SymBool, SymInt, SymFloat, int, bool, float]
) -> Union[bool, int, float]:
    if isinstance(a, (SymBool, bool)):
        return guard_bool(a)
    elif isinstance(a, (SymInt, int)):
        return guard_int(a)
    elif isinstance(a, (SymFloat, float)):
        return guard_float(a)
    else:
        raise AssertionError(f"unrecognized scalar {a}")
