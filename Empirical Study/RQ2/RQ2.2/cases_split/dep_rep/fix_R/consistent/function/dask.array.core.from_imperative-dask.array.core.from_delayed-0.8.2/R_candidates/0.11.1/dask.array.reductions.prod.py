@wraps(chunk.prod)
def prod(a, axis=None, dtype=None, keepdims=False, split_every=None):
    if dtype is not None:
        dt = dtype
    elif a._dtype is not None:
        dt = np.empty((1,), dtype=a._dtype).prod().dtype
    else:
        dt = None
    return reduction(a, chunk.prod, chunk.prod, axis=axis, keepdims=keepdims,
                     dtype=dt, split_every=split_every)
