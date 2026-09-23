def is_concrete_bool(a: Union[bool, SymBool]) -> bool:
    """
    Utility to check if underlying object
    in SymBool is concrete value. Also returns
    true if integer is passed in.

    Args:
        a (SymBool or bool): Object to test if it bool
    """
    assert isinstance(a, (SymBool, bool))

    if isinstance(a, bool):
        return True

    if isinstance(
        a.node.expr, (sympy.logic.boolalg.BooleanTrue, sympy.logic.boolalg.BooleanFalse)
    ):
        return True

    return False
