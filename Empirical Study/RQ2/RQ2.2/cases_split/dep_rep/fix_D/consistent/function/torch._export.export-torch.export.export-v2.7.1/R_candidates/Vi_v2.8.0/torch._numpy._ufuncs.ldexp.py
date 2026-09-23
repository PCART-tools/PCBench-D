@normalizer
def ldexp(
    x1: ArrayLikeOrScalar,
    x2: ArrayLikeOrScalar,
    /,
    out: Optional[OutArray] = None,
    *,
    where: NotImplementedType = True,
    casting: Optional[CastingModes] = "same_kind",
    order: NotImplementedType = "K",
    dtype: Optional[DTypeLike] = None,
    subok: NotImplementedType = False,
    signature: NotImplementedType = None,
    extobj: NotImplementedType = None,
):
    if dtype is not None:
        if isinstance(x1, torch.Tensor):
            x1 = _util.typecast_tensor(x1, dtype, casting)
        else:
            x1 = torch.as_tensor(x1, dtype=dtype)
    else:
        if not isinstance(x1, torch.Tensor):
            x1 = torch.as_tensor(x1)
            x1 = _util.cast_int_to_float(x1)

    x2 = torch.as_tensor(x2)
    # the second arg must be integer
    if _dtypes_impl._category(x2.dtype) != 1:
        raise ValueError("ldexp 2nd arg must be integer")

    result = _binary_ufuncs_impl.ldexp(x1, x2)

    if x1.dtype == torch.float16:
        # torch.ldexp(f16, int) -> f32, undo it
        result = result.to(torch.float16)

    return _ufunc_postprocess(result, out, casting)
