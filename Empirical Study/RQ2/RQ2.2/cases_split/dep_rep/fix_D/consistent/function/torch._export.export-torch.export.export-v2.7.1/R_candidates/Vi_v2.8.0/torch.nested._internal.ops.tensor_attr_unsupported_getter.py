@register_jagged_func(
    [torch.ops.aten.size.default],
    "self: jt_all",
)
def tensor_attr_unsupported_getter(func, *args, **kwargs):
    if func == torch.ops.aten.size.default:
        raise RuntimeError(
            "NestedTensor does not support directly calling torch.ops.aten.size; "
            "please use `nested_tensor.size()` instead."
        )
