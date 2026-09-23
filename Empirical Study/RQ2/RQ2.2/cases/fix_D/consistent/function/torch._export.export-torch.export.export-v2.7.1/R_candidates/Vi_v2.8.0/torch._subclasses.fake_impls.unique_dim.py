@register_op_impl(aten.unique_dim.default)
def unique_dim(
    fake_mode, func, arg, dim, sorted=True, return_inverse=False, return_counts=False
):
    return _unique(
        fake_mode,
        func,
        arg,
        # normalize dim to be non-negative
        dim if dim >= 0 else dim % max(arg.ndim, 1),
        sorted,
        return_inverse,
        return_counts,
    )
