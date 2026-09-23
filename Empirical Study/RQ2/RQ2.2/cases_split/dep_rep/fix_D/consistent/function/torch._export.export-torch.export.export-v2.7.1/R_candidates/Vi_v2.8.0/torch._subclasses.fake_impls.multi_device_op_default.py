@register_op_impl(aten._unsafe_index_put.default)
@register_op_impl(aten.copy.default)
@register_op_impl(aten.copy_.default)
@register_op_impl(aten.slice_scatter.default)
def multi_device_op_default(fake_mode, func, *args, **kwargs):
    return run_and_return_new_tensor_of_input_device(fake_mode, func, args, kwargs)
