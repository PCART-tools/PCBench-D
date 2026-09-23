def cast_symbool_to_symint_guardless(
    symbool: Union[bool, torch.SymBool],
) -> Union[int, torch.SymInt]:
    """
    Converts a SymBool or bool to a SymInt or int without introducing guards.

    This function maps True to 1 and False to 0, preserving the symbolic nature
    of the input when it's a SymBool. Unlike regular casting which might introduce
    guards, this function performs the conversion without adding any guards.

    Args:
        symbool: A boolean value, either a concrete bool or symbolic SymBool

    Returns:
        The corresponding integer value (1 for True, 0 for False) as either
        a concrete int or symbolic SymInt
    """
    if isinstance(symbool, bool):
        return 1 if symbool else 0
    int_sym = _sympy_cast_symbool_to_symint_guardless(symbool.node.expr)
    return symbool.node.shape_env.create_symintnode(
        int_sym, hint=int(symbool.node.require_hint()) if has_hint(symbool) else None
    )
