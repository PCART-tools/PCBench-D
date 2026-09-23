@normalizer
def divmod(
    x1: ArrayLike,
    x2: ArrayLike,
    out1: Optional[OutArray] = None,
    out2: Optional[OutArray] = None,
    /,
    out: tuple[Optional[OutArray], Optional[OutArray]] = (None, None),
    *,
    where: NotImplementedType = True,
    casting: Optional[CastingModes] = "same_kind",
    order: NotImplementedType = "K",
    dtype: Optional[DTypeLike] = None,
    subok: NotImplementedType = False,
    signature: NotImplementedType = None,
    extobj: NotImplementedType = None,
):
    # make sure we either have no out arrays at all, or there is either
    # out1, out2, or out=tuple, but not both
    num_outs = sum(x is not None for x in [out1, out2])
    if num_outs == 1:
        raise ValueError("both out1 and out2 need to be provided")
    elif num_outs == 2:
        o1, o2 = out
        if o1 is not None or o2 is not None:
            raise TypeError(
                "cannot specify 'out' as both a positional and keyword argument"
            )
    else:
        out1, out2 = out

    if dtype is None:
        dtype = _dtypes_impl.result_type_impl(x1, x2)
    x1, x2 = _util.typecast_tensors((x1, x2), dtype, casting)

    quot, rem = _binary_ufuncs_impl.divmod(x1, x2)

    quot = _ufunc_postprocess(quot, out1, casting)
    rem = _ufunc_postprocess(rem, out2, casting)
    return quot, rem
