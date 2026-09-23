def take(
    a: ArrayLike,
    indices: ArrayLike,
    axis=None,
    out: Optional[OutArray] = None,
    mode: NotImplementedType = "raise",
):
    (a,), axis = _util.axis_none_flatten(a, axis=axis)
    axis = _util.normalize_axis_index(axis, a.ndim)
    idx = (slice(None),) * axis + (indices, ...)
    result = a[idx]
    return result
