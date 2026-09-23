@normalizer
def matmul(
    x1: ArrayLike,
    x2: ArrayLike,
    /,
    out: Optional[OutArray] = None,
    *,
    casting: Optional[CastingModes] = "same_kind",
    order: NotImplementedType = "K",
    dtype: Optional[DTypeLike] = None,
    subok: NotImplementedType = False,
    signature: NotImplementedType = None,
    extobj: NotImplementedType = None,
    axes: NotImplementedType = None,
    axis: NotImplementedType = None,
):
    if dtype is None:
        dtype = _dtypes_impl.result_type_impl(x1, x2)
    x1, x2 = _util.typecast_tensors((x1, x2), dtype, casting)

    result = _binary_ufuncs_impl.matmul(x1, x2)

    result = _ufunc_postprocess(result, out, casting)
    return result
