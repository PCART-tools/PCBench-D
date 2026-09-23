@register_op_impl(aten._unique2.default)
def unique2(
    fake_mode, func, arg, sorted=True, return_inverse=False, return_counts=False
):
    return _unique(fake_mode, func, arg, None, sorted, return_inverse, return_counts)
