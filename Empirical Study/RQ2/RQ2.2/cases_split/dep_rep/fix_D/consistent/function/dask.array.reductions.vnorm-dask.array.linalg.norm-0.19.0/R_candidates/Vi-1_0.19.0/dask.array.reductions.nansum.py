@wraps(chunk.nansum)
def nansum(a, axis=None, dtype=None, keepdims=False, split_every=None, out=None):
    if dtype is not None:
        dt = dtype
    else:
        dt = getattr(chunk.nansum(np.empty((1,), dtype=a.dtype)), 'dtype', object)
    return reduction(a, chunk.nansum, chunk.sum, axis=axis, keepdims=keepdims,
                     dtype=dt, split_every=split_every, out=out)
