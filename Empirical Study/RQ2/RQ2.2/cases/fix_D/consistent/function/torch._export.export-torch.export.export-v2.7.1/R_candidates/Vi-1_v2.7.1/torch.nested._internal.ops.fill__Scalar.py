@register_jagged_func(torch.ops.aten.fill_.Scalar, "self: jt_all, value: any")
def fill__Scalar(func, *args, **kwargs):
    _, new_kwargs = normalize_function(  # type: ignore[misc]
        func, args=args, kwargs=kwargs, normalize_to_only_use_kwargs=True
    )

    inp = new_kwargs.pop("input")

    func(inp._values, **new_kwargs)
    return inp
