def nanvar(a, axis=None, dtype=None, keepdims=False, ddof=0, split_every=None,
           out=None):
    if dtype is not None:
        dt = dtype
    else:
        dt = getattr(np.var(np.ones(shape=(1,), dtype=a.dtype)), 'dtype', object)
    return reduction(a, partial(moment_chunk, sum=chunk.nansum, numel=nannumel),
                     partial(moment_agg, sum=np.nansum, ddof=ddof), axis=axis,
                     keepdims=keepdims, dtype=dt, split_every=split_every,
                     combine=partial(moment_combine, sum=np.nansum), out=out)
