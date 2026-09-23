@wraps(chunk.var)
def var(a, axis=None, dtype=None, keepdims=False, ddof=0, split_every=None):
    if dtype is not None:
        dt = dtype
    elif a._dtype is not None:
        dt = np.var(np.ones(shape=(1,), dtype=a._dtype)).dtype
    else:
        dt = None
    return reduction(a, moment_chunk, partial(moment_agg, ddof=ddof), axis=axis,
                     keepdims=keepdims, dtype=dt, split_every=split_every,
                     combine=moment_combine, name='var')
