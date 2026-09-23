def trace(
    a: ArrayLike,
    offset=0,
    axis1=0,
    axis2=1,
    dtype: Optional[DTypeLike] = None,
    out: Optional[OutArray] = None,
):
    result = torch.diagonal(a, offset, dim1=axis1, dim2=axis2).sum(-1, dtype=dtype)
    return result
