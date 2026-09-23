@register_jagged_func(torch.ops.aten.any.dims, "self: jt_all, dim: any?, keepdim: any?")
def any_dims(func, *args, **kwargs):
    return _apply_reduction(func, "any", False, *args, **kwargs)
