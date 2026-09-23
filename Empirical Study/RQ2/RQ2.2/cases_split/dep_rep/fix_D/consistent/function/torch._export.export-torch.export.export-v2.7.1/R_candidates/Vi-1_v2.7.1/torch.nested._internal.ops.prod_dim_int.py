@register_jagged_func(
    torch.ops.aten.prod.dim_int,
    "self: jt_all, dim: any, keepdim: any?, dtype: any?",
)
def prod_dim_int(func, *args, **kwargs):
    return _apply_reduction(func, "prod", 1, *args, **kwargs)
