def _is_non_negative_check(cond: sympy.Basic) -> Optional[str]:
    """
    Check if a condition (SymPy expression) is checking for non-negative values (>= 0).
    Returns the variable name if it's a non-negative check (>= 0), None otherwise.
    """
    if isinstance(cond, sympy.Rel):
        if cond.rel_op == ">=" and cond.rhs == 0:
            return str(cond.lhs)
    return None
