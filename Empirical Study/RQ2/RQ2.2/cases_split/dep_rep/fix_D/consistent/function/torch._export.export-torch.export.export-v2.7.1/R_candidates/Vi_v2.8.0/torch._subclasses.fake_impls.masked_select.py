@register_op_impl(torch.ops.aten.masked_select.default)
def masked_select(fake_mode, func, self, mask):
    if (
        fake_mode.shape_env is None
        or not fake_mode.shape_env.allow_dynamic_output_shape_ops
    ):
        # Without symints/symfloats, cannot handle this
        raise DynamicOutputShapeException(func)

    nnz = fake_mode.shape_env.create_unbacked_symint()

    # see nonzero for commentary
    maxval = sys.maxsize - 1

    # Avoid importing sympy at a module level
    from torch.fx.experimental.symbolic_shapes import (
        _constrain_range_for_size,
        has_free_symbols,
    )
    from torch.utils._sympy.numbers import IntInfinity
    from torch.utils._sympy.value_ranges import bound_sympy

    # If num elements is expressed symbolically, calculate
    # the concrete value based on upper bounds. Otherwise,
    # we can set max val directly.
    if not has_free_symbols(self.numel()):
        num_elements = int(self.numel())
    else:
        prod_node = math.prod(self.shape).node
        prod_range = bound_sympy(prod_node.expr, prod_node.shape_env.var_to_range)
        if isinstance(prod_range.upper, IntInfinity):
            num_elements = sys.maxsize - 1
        else:
            num_elements = prod_range.upper
    if num_elements > 2:
        maxval = num_elements

    _constrain_range_for_size(nnz, max=maxval)

    return self.new_empty((nnz,))
