def moment(a, order, axis=None, dtype=None, keepdims=False, ddof=0,
           split_every=None, out=None):
    if not isinstance(order, int) or order < 0:
        raise ValueError("Order must be an integer >= 0")

    if order < 2:
        reduced = a.sum(axis=axis)   # get reduced shape and chunks
        if order == 0:
            # When order equals 0, the result is 1, by definition.
            return ones(reduced.shape, chunks=reduced.chunks, dtype='f8')
        # By definition the first order about the mean is 0.
        return zeros(reduced.shape, chunks=reduced.chunks, dtype='f8')

    if dtype is not None:
        dt = dtype
    else:
        dt = getattr(np.var(np.ones(shape=(1,), dtype=a.dtype)), 'dtype', object)
    return reduction(a, partial(moment_chunk, order=order),
                     partial(moment_agg, order=order, ddof=ddof),
                     axis=axis, keepdims=keepdims,
                     dtype=dt, split_every=split_every, out=out,
                     combine=partial(moment_combine, order=order))
