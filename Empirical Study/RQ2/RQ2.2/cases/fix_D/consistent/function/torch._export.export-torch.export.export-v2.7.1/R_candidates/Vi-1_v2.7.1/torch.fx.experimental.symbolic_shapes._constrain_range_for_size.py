def _constrain_range_for_size(
    a: SymInt, min: Optional[int] = None, max: Optional[int] = None
) -> None:
    """
    This function is NOT INTENDED to be used by itself.
    """

    if isinstance(a, (SymFloat, SymBool)):
        raise ValueError("Constraining SymFloat/SymBool is nyi")

    assert isinstance(a, SymInt), "can only constrain range for SymInt"
    assert isinstance(a.node.expr, sympy.Symbol), f"constraining non-Symbols NYI: {a}"

    a.node.shape_env._constrain_range_for_size(a.node.expr, min, max)
