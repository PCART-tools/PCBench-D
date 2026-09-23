@wraps(chunk.sum)
def sum(a, axis=None, dtype=None, keepdims=False, split_every=None, out=None):
    if dtype is not None:
        dt = dtype
    else:
        dt = getattr(np.empty((1,), dtype=a.dtype).sum(), 'dtype', object)
    return reduction(a, chunk.sum, chunk.sum, axis=axis, keepdims=keepdims,
                     dtype=dt, split_every=split_every, out=out)
