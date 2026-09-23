@register_op_impl(_is_tensor_constructor)
@register_op_impl([*_like_tensor_constructors])
def constructors(fake_mode, func, *args, **kwargs):
    assert func not in _non_kwarg_device_constructors
    _, new_kwargs = normalize_function(
        func, args=args, kwargs=kwargs, normalize_to_only_use_kwargs=True
    )
    if "names" in kwargs:
        raise UnsupportedOperatorException(
            "torch.compile doesn't support named tensors"
        )

    if func in _like_tensor_constructors:
        default_device = new_kwargs["input"].device
        # TODO: file issue
        args = (new_kwargs.pop("input"),)
    else:
        # cpu is default device if none is specified
        default_device = torch.device("cpu")
        args = ()
    out_device = new_kwargs.pop("device", None)
    out_device = out_device if out_device is not None else default_device
    new_kwargs["device"] = torch.device("meta")
    # _like constructors have fake tensor inputs (maybe this causes the non-like
    # to fail? hmmm)
    with in_kernel_invocation_manager(fake_mode):
        r = func(*args, **new_kwargs)
    return FakeTensor(fake_mode, r, out_device)
