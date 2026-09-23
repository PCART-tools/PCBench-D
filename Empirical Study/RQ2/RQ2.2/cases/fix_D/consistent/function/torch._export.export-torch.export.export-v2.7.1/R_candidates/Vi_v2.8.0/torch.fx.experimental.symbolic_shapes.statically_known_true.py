def statically_known_true(x: BoolLikeType) -> bool:
    """
    Returns True if x can be simplified to a constant and is true.

    .. note::
        This function doesn't introduce new guards, so the expression may end
        up evaluating to true at runtime even if this function returns False.

    Args:
        x (bool, SymBool): The expression to try statically evaluating
    """
    if not isinstance(x, SymBool):
        assert isinstance(x, bool)
        return x

    result = _static_eval_sym_bool(x)
    if result is None:
        return False

    return result
