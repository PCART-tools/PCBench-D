def percentile(
    a: ArrayLike,
    q: ArrayLike,
    axis: AxisLike = None,
    out: Optional[OutArray] = None,
    overwrite_input=False,
    method="linear",
    keepdims: KeepDims = False,
    *,
    interpolation: NotImplementedType = None,
):
    # np.percentile(float_tensor, 30) : q.dtype is int64 => q / 100.0 is float32
    if _dtypes_impl.python_type_for_torch(q.dtype) == int:
        q = q.to(_dtypes_impl.default_dtypes().float_dtype)
    qq = q / 100.0

    return quantile(
        a,
        qq,
        axis=axis,
        overwrite_input=overwrite_input,
        method=method,
        keepdims=keepdims,
        interpolation=interpolation,
    )
