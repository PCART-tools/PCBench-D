@register_jagged_func(
    [
        torch.ops.aten.all.default,
        torch.ops.aten.any.default,
        torch.ops.aten.max.default,
        torch.ops.aten.min.default,
    ],
    "self: jt_all",
)
def all_any_max_min_default(func, *args, **kwargs):
    _, new_kwargs = normalize_function(  # type: ignore[misc]
        func, args=args, kwargs=kwargs, normalize_to_only_use_kwargs=True
    )

    inp = new_kwargs.pop("input")

    return func(inp._values, **new_kwargs)
