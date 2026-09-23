def maybe_layout_constraints(fn: Callable[..., Any]) -> Optional[Callable[..., Any]]:
    """Get layout constraints. Returns None if there are no layout constraints."""
    if not isinstance(fn, torch._ops.OpOverload):
        # Only OpOverloads have layout constraints.
        return None
    if fn in _maybe_layout_constraints:
        return _maybe_layout_constraints[fn]
    # OpOverload with custom lowerings override tag-based layout constraints
    if fn in lowerings:
        _maybe_layout_constraints[fn] = None
        return None
    # We lazily register tag-based layout constraints.

    def handle_layout_constraint_tag(tag):
        if tag is torch._C.Tag.needs_fixed_stride_order:
            _maybe_layout_constraints[fn] = constrain_to_fx_strides
            return _maybe_layout_constraints[fn]
        elif tag is torch._C.Tag.flexible_layout:
            _maybe_layout_constraints[fn] = None
            return None
        else:
            raise AssertionError(f"Unknown layout constraint tag: {tag}")

    tag = get_layout_constraint_tag(fn)
    return handle_layout_constraint_tag(tag)
