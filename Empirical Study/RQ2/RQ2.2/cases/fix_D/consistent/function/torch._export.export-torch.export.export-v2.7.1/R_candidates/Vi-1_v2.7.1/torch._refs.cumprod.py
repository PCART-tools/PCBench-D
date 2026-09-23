@register_decomposition(aten.cumprod)
def cumprod(
    a: TensorLikeType,
    dim: int,
    *,
    dtype: Optional[torch.dtype] = None,
    out: Optional[Tensor] = None,
) -> TensorLikeType:
    return _cumsumprod_common(func=prod, init=1, a=a, dim=dim, dtype=dtype, out=out)
