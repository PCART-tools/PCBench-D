def statically_known_true(x: Union[bool, SymBool]) -> bool:
    """
    Returns True if x can be simplified to a constant and is true.

    .. note::
        This function doesn't introduce new guards, so the expression may end
        up evaluating to true at runtime even if this function returns False.

    Args:
        x (bool, SymBool): The expression to try statically evaluating
    """
    if isinstance(x, SymBool):
        expr = x.node.expr
        shape_env = x.node.shape_env
        try:
            simplified = shape_env._maybe_evaluate_static(expr)
            if simplified is not None:
                return bool(simplified)
        except Exception:
            log.debug("Could not simplify %s", expr)
        return False
    assert isinstance(x, bool)
    return x
