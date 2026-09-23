@register_meta([aten.full.default])
def full(size, fill_value, *args, **kwargs):
    dtype = kwargs.get("dtype", None)
    if not dtype:
        dtype = utils.get_dtype(fill_value)
    kwargs["dtype"] = dtype
    return torch.empty(size, *args, **kwargs)
