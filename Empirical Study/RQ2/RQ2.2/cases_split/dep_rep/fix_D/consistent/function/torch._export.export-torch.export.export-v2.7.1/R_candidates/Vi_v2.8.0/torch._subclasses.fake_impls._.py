@register_op_impl(aten.unique_consecutive.default)
def _(fake_mode, func, arg, return_inverse=False, return_counts=False, dim=None):
    return _unique(
        fake_mode,
        func,
        arg,
        dim,
        False,
        return_inverse,
        return_counts,
        unique_consecutive=True,
    )
