def _get_symint_hints(exprs):
    """
    Get the hints of a list/tuple of int/SymInt.
    """
    if isinstance(exprs, (list, tuple)):
        return type(exprs)(_get_symint_hints(e) for e in exprs)
    elif isinstance(exprs, torch.SymInt):
        return exprs.node.shape_env.size_hint(exprs.node.expr)
    else:
        return exprs
