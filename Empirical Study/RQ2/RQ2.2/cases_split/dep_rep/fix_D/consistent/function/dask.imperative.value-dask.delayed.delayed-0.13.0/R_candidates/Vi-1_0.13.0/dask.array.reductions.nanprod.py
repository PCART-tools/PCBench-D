    @wraps(chunk.nanprod)
    def nanprod(a, axis=None, dtype=None, keepdims=False, split_every=None):
        if dtype is not None:
            dt = dtype
        else:
            dt = chunk.nanprod(np.empty((1,), dtype=a.dtype)).dtype
        return reduction(a, chunk.nanprod, chunk.prod, axis=axis,
                         keepdims=keepdims, dtype=dt, split_every=split_every)
