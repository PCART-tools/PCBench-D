def moment(a, order, axis=None, dtype=None, keepdims=False, ddof=0,
           split_every=None):
    if not isinstance(order, int) or order < 2:
        raise ValueError("Order must be an integer >= 2")
    if dtype is not None:
        dt = dtype
    elif a._dtype is not None:
        dt = np.var(np.ones(shape=(1,), dtype=a._dtype)).dtype
    else:
        dt = None
    return reduction(a, partial(moment_chunk, order=order),
                     partial(moment_agg, order=order, ddof=ddof),
                     axis=axis, keepdims=keepdims,
                     dtype=dt, split_every=split_every,
                     combine=partial(moment_combine, order=order))
