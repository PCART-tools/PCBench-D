@register_jagged_func(
    [
        torch.ops.aten.new_empty.default,
        torch.ops.aten.new_zeros.default,
        torch.ops.aten.new_ones.default,
    ],
    "self: jt_all, size: any, dtype: any?, layout: any?, device: any?, pin_memory: any?",
)
def new_empty_default(func, *args, **kwargs):
    _, new_kwargs = normalize_function(  # type: ignore[misc]
        func, args=args, kwargs=kwargs, normalize_to_only_use_kwargs=True
    )

    inp = new_kwargs.pop("input")

    if len(new_kwargs["size"]) == 0:
        return func(inp._values, **new_kwargs)

    raise RuntimeError("new_empty() not supported for NJT with shape != ()")
