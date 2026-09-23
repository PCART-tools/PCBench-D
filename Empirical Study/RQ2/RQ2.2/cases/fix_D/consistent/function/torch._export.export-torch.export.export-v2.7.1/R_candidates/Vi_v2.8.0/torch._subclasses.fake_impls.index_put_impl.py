@register_op_impl(aten.index_put.default)
@register_op_impl(aten.index_put_.default)
def index_put_impl(fake_mode, func, *args, **kwargs):
    _, new_kwargs = normalize_function(
        func, args=args, kwargs=kwargs, normalize_to_only_use_kwargs=True
    )

    values = new_kwargs["values"]
    self_device = new_kwargs["input"].fake_device
    torch._check(
        self_device == values.fake_device or (values.ndim == 0 and values.numel() == 1),
        lambda: f"Mismatching {func} device between self ({self_device}) and values ({values.device})",
    )

    out = run_and_return_new_tensor_of_input_device(fake_mode, func, args, kwargs)
    if func is aten.index_put_.default:
        return new_kwargs["input"]
    else:
        return out
