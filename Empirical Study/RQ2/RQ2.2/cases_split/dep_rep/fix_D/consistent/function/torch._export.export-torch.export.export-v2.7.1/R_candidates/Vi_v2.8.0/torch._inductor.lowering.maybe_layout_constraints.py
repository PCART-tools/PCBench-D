def maybe_layout_constraints(fn: Callable[..., Any]) -> Optional[Callable[..., Any]]:
    """Get layout constraints. Returns None if there are no layout constraints."""
    if not isinstance(fn, torch._ops.OpOverload):
        # Only OpOverloads have layout constraints.
        return None
    if fn in _maybe_layout_constraints:
        return _maybe_layout_constraints[fn]
    return None
