@register_jagged_func(
    torch.ops.aten.argmax.default, "self: jt_all, dim: any?, keepdim: any?"
)
def argmax_default(func, *args, **kwargs):
    _, new_kwargs = normalize_function(  # type: ignore[misc]
        func, args=args, kwargs=kwargs, normalize_to_only_use_kwargs=True
    )

    dtype_min = torch.finfo(new_kwargs["input"].dtype).min
    return _apply_reduction(func, "argmax", dtype_min, *args, **kwargs)
