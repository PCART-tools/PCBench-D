@register_op_impl(aten.copy.out)
@register_op_impl(aten.slice_scatter.out)
def multi_device_op_out(fake_mode, func, *args, **kwargs):
    with in_kernel_invocation_manager(fake_mode):
        func(*args, **kwargs)

    _, new_kwargs = normalize_function(
        func, args=args, kwargs=kwargs, normalize_to_only_use_kwargs=True
    )

    return new_kwargs["input"]
