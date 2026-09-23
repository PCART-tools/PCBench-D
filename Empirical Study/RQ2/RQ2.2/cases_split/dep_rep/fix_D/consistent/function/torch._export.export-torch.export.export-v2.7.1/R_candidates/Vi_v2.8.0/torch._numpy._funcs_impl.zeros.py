def zeros(
    shape,
    dtype: Optional[DTypeLike] = None,
    order: NotImplementedType = "C",
    *,
    like: NotImplementedType = None,
):
    if dtype is None:
        dtype = _dtypes_impl.default_dtypes().float_dtype
    return torch.zeros(shape, dtype=dtype)
