def is_concrete_float(a: FloatLikeType) -> bool:
    r"""Utility to check if underlying object
    in SymInt is concrete value. Also returns
    true if integer is passed in.

    Args:
        a (SymInt or float): Object to test if it float
    """
    assert isinstance(a, (SymFloat, float))

    if isinstance(a, float):
        return True

    if isinstance(a.node.expr, sympy.core.numbers.Float):
        return True

    return False
