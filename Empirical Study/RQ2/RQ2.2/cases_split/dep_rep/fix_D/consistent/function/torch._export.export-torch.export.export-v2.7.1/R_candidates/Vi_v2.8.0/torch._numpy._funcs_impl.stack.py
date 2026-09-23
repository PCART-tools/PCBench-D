def stack(
    arrays: Sequence[ArrayLike],
    axis=0,
    out: Optional[OutArray] = None,
    *,
    dtype: Optional[DTypeLike] = None,
    casting: Optional[CastingModes] = "same_kind",
):
    _concat_check(arrays, dtype, out=out)

    tensors = _concat_cast_helper(arrays, dtype=dtype, casting=casting)
    result_ndim = tensors[0].ndim + 1
    axis = _util.normalize_axis_index(axis, result_ndim)
    return torch.stack(tensors, axis=axis)
