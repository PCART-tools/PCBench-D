def has_static_value(a: Union[SymBool, SymFloat, SymInt, bool, float, int]) -> bool:
    """
    User-code friendly utility to check if a value is static or dynamic.
    Returns true if given a constant, or a symbolic expression with a fixed value.

    Args:
        a (Union[SymBool, SymFloat, SymInt, bool, float, int]): Object to test
    """
    assert isinstance(a, BoolLike + FloatLike + IntLike)
    if (
        isinstance(a, BoolLike)
        and is_concrete_bool(a)  # type: ignore[arg-type]
        or isinstance(a, FloatLike)
        and is_concrete_float(a)  # type: ignore[arg-type]
        or isinstance(a, IntLike)
        and is_concrete_int(a)  # type: ignore[arg-type]
    ):
        return True

    assert isinstance(a, py_sym_types)
    return a.node.shape_env.bound_sympy(a.node.expr).is_singleton()  # type: ignore[union-attr]
