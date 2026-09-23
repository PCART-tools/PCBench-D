@wraps(chunk.var)
def var(a, axis=None, dtype=None, keepdims=False, ddof=0, split_every=None,
        out=None):
    if dtype is not None:
        dt = dtype
    else:
        dt = getattr(np.var(np.ones(shape=(1,), dtype=a.dtype)), 'dtype', object)
    return reduction(a, moment_chunk, partial(moment_agg, ddof=ddof), axis=axis,
                     keepdims=keepdims, dtype=dt, split_every=split_every,
                     combine=moment_combine, name='var', out=out)
