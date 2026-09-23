def concatenate(
    ar_tuple: Sequence[ArrayLike],
    axis=0,
    out: Optional[OutArray] = None,
    dtype: Optional[DTypeLike] = None,
    casting: Optional[CastingModes] = "same_kind",
):
    _concat_check(ar_tuple, dtype, out=out)
    result = _concatenate(ar_tuple, axis=axis, out=out, dtype=dtype, casting=casting)
    return result
