@register_jagged_func(torch.ops.aten.broadcast_to.default, "self: jt_all, size: any")
def broadcast_to(func, *args, **kwargs):
    _, new_kwargs = normalize_function(  # type: ignore[misc]
        func, args=args, kwargs=kwargs, normalize_to_only_use_kwargs=True
    )

    inp = new_kwargs.pop("input")
    size = new_kwargs.pop("size")

    if len(size) <= inp.dim():
        return inp.expand([*(1 for _ in range(inp.dim() - len(size))), *size])

    raise ValueError(
        "broadcast_to(): broadcasting to a higher-dim shape is currently not supported "
        "for nested tensors with the jagged layout"
    )
