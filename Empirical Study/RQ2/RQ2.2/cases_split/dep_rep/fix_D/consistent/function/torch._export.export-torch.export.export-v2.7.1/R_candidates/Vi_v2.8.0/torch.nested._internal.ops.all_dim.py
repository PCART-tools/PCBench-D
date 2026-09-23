@register_jagged_func(torch.ops.aten.all.dim, "self: jt_all, dim: any, keepdim: any?")
def all_dim(func, *args, **kwargs):
    _, new_kwargs = normalize_function(  # type: ignore[misc]
        func, args=args, kwargs=kwargs, normalize_to_only_use_kwargs=True
    )

    # wrap dim in list to redispatch to dims overload
    new_kwargs["dim"] = [new_kwargs["dim"]]
    return all_dims(torch.ops.aten.all.dims, **new_kwargs)
