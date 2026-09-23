@wraps(chunk.sum)
def sum(a, axis=None, dtype=None, keepdims=False, split_every=None):
    if dtype is not None:
        dt = dtype
    elif a._dtype is not None:
        dt = np.empty((1,), dtype=a._dtype).sum().dtype
    else:
        dt = None
    return reduction(a, chunk.sum, chunk.sum, axis=axis, keepdims=keepdims,
                     dtype=dt, split_every=split_every)
