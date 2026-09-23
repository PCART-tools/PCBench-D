@register_jagged_func(
    torch.ops.aten.expand.default, "self: jt_all, size: any, implicit: any?"
)
def expand_default(func, *args, **kwargs):
    _, new_kwargs = normalize_function(  # type: ignore[misc]
        func, args=args, kwargs=kwargs, normalize_to_only_use_kwargs=True
    )

    inp = new_kwargs.pop("input")
    size = new_kwargs["size"]

    assert ("implicit" not in new_kwargs) or (not new_kwargs.pop("implicit"))
    if not raggedness_matches(inp, size):
        raise RuntimeError(f"expand(): cannot expand shape {inp._size} -> {size}")

    expand_arg = [-1 if d == inp._ragged_idx else size[d] for d in range(1, inp.dim())]
    return NestedTensor(func(inp._values, expand_arg), **extract_kwargs(inp))
