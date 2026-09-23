def _get_counts(mask, axis, dtype=float):
    dtype = _get_dtype(dtype)
    if axis is None:
        return dtype.type(mask.size - mask.sum())

    count = mask.shape[axis] - mask.sum(axis)
    if is_scalar(count):
        return dtype.type(count)
    try:
        return count.astype(dtype)
    except AttributeError:
        return np.array(count, dtype=dtype)
