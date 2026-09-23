@register_jagged_func(torch.ops.aten.min.dim, "self: jt_all, dim: any, keepdim: any?")
def min_dim(func, *args, **kwargs):
    _, new_kwargs = normalize_function(  # type: ignore[misc]
        func, args=args, kwargs=kwargs, normalize_to_only_use_kwargs=True
    )

    dtype_max = torch.finfo(new_kwargs["input"].dtype).max
    return _apply_reduction(func, "min", dtype_max, *args, **kwargs)
