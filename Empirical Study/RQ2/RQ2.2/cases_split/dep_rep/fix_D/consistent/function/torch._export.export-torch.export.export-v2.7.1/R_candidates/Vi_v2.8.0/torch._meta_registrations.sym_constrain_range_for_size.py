@register_meta(aten.sym_constrain_range_for_size.default)
def sym_constrain_range_for_size(size, min=None, max=None):
    # Avoid importing sympy at a module level
    from torch.fx.experimental.symbolic_shapes import _constrain_range_for_size

    if min is None and max is None:
        torch._check_is_size(size)
        return

    if isinstance(size, (SymFloat, SymBool)):
        raise ValueError("Constraining SymFloat or Symbool is nyi")
    if type(size) is int:
        if min is not None:
            torch._check(size >= min)
        if max is not None:
            torch._check(size <= max)
        return
    _constrain_range_for_size(size, min=min, max=max)
