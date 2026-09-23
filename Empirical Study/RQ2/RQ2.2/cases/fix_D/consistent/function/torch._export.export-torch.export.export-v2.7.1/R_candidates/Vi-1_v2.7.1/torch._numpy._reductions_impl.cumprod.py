def cumprod(
    a: ArrayLike,
    axis: AxisLike = None,
    dtype: Optional[DTypeLike] = None,
    out: Optional[OutArray] = None,
):
    if dtype == torch.bool:
        dtype = _dtypes_impl.default_dtypes().int_dtype
    if dtype is None:
        dtype = a.dtype

    (a,), axis = _util.axis_none_flatten(a, axis=axis)
    axis = _util.normalize_axis_index(axis, a.ndim)

    return a.cumprod(axis=axis, dtype=dtype)
