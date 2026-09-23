@wraps(chunk.prod)
def prod(a, axis=None, dtype=None, keepdims=False, split_every=None):
    if dtype is not None:
        dt = dtype
    else:
        dt = np.empty((1,), dtype=a.dtype).prod().dtype
    return reduction(a, chunk.prod, chunk.prod, axis=axis, keepdims=keepdims,
                     dtype=dt, split_every=split_every)
