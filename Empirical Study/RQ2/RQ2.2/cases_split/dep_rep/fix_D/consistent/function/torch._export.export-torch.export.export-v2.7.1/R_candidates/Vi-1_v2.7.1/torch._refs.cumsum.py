@register_decomposition(aten.cumsum)
def cumsum(
    a: TensorLikeType,
    dim: int,
    *,
    dtype: Optional[torch.dtype] = None,
    out: Optional[Tensor] = None,
) -> TensorLikeType:
    return _cumsumprod_common(func=sum, init=0, a=a, dim=dim, dtype=dtype, out=out)
