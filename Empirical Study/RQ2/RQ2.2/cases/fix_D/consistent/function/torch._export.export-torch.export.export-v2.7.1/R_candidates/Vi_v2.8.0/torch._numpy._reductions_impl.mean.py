@_deco_axis_expand
def mean(
    a: ArrayLike,
    axis: AxisLike = None,
    dtype: Optional[DTypeLike] = None,
    out: Optional[OutArray] = None,
    keepdims: KeepDims = False,
    *,
    where: NotImplementedType = None,
):
    dtype = _atleast_float(dtype, a.dtype)

    axis_kw = {} if axis is None else {"dim": axis}
    result = a.mean(dtype=dtype, **axis_kw)

    return result
