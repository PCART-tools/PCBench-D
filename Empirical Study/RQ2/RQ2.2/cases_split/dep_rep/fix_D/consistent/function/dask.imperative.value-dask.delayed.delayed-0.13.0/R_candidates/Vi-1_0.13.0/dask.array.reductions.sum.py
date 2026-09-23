@wraps(chunk.sum)
def sum(a, axis=None, dtype=None, keepdims=False, split_every=None):
    if dtype is not None:
        dt = dtype
    else:
        dt = np.empty((1,), dtype=a.dtype).sum().dtype
    return reduction(a, chunk.sum, chunk.sum, axis=axis, keepdims=keepdims,
                     dtype=dt, split_every=split_every)
