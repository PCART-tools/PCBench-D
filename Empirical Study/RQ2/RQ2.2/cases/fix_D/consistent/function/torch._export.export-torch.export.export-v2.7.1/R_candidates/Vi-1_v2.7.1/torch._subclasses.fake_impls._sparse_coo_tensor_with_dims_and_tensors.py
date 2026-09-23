@register_op_impl(aten._sparse_coo_tensor_with_dims_and_tensors.default)
def _sparse_coo_tensor_with_dims_and_tensors(fake_mode, func, *args, **kwargs):
    # TODO: remove me
    return constructors(fake_mode, func, *args, **kwargs)
