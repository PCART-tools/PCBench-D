@register_jagged_func(torch.ops.aten.all.dims, "self: jt_all, dim: any?, keepdim: any?")
def all_dims(func, *args, **kwargs):
    return _apply_reduction(func, "all", True, *args, **kwargs)
