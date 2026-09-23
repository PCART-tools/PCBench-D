@register_decomposition(aten.var_mean)
@out_wrapper("out0", "out1")
def var_mean(
    a: TensorLikeType,
    dim: Optional[DimsType] = None,
    unbiased: Optional[bool] = None,
    keepdim: bool = False,
    *,
    correction: Optional[NumberType] = None,
):
    dim, unbiased = _dim_var_dispatch(dim, unbiased)
    v = var(a, dim, unbiased, keepdim, correction=correction)
    m = mean(a, dim, keepdim)
    return v, m
