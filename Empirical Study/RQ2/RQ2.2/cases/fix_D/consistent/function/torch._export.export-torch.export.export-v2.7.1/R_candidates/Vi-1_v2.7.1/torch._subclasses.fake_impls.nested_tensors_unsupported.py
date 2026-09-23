@register_op_impl(aten._nested_tensor_from_tensor_list.default)
@register_op_impl(aten._nested_tensor_from_tensor_list.out)
@register_op_impl(aten._nested_view_from_buffer.default)
@register_op_impl(aten._nested_view_from_buffer_copy.default)
def nested_tensors_unsupported(fake_mode, func, *args, **kwargs):
    raise UnsupportedOperatorException(
        "torch.compile does not support strided NestedTensor"
    )
