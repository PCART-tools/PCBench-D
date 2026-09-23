@register_jagged_func(torch.ops.aten.max.dim, "self: jt_all, dim: any, keepdim: any?")
def max_dim(func, *args, **kwargs):
    _, new_kwargs = normalize_function(  # type: ignore[misc]
        func, args=args, kwargs=kwargs, normalize_to_only_use_kwargs=True
    )

    dtype_min = torch.finfo(new_kwargs["input"].dtype).min
    return _apply_reduction(func, "max", dtype_min, *args, **kwargs)
