@register_op_impl(
    [
        x
        for x in _device_not_kwarg_ops
        if x
        not in (
            # these are already registered elsewhere
            aten.is_pinned.default,
            aten.to.device,
            aten.to.prim_Device,
            aten._nested_tensor_from_tensor_list.default,
            aten._nested_tensor_from_tensor_list.out,
        )
    ]
)
def nyi(fake_mode, func, *args, **kwargs):
    assert func not in _device_not_kwarg_ops, f"NYI: {func}"
