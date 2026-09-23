@wraps(chunk.nansum)
def nansum(a, axis=None, dtype=None, keepdims=False, split_every=None):
    if dtype is not None:
        dt = dtype
    else:
        dt = chunk.nansum(np.empty((1,), dtype=a.dtype)).dtype
    return reduction(a, chunk.nansum, chunk.sum, axis=axis, keepdims=keepdims,
                     dtype=dt, split_every=split_every)
