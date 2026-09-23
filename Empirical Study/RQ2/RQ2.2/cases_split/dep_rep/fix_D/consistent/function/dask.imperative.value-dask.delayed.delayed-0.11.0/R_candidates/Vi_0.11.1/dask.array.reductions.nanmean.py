def nanmean(a, axis=None, dtype=None, keepdims=False, split_every=None):
    if dtype is not None:
        dt = dtype
    elif a._dtype is not None:
        dt = np.mean(np.empty(shape=(1,), dtype=a._dtype)).dtype
    else:
        dt = None
    return reduction(a, partial(mean_chunk, sum=chunk.nansum, numel=nannumel),
                     mean_agg, axis=axis, keepdims=keepdims, dtype=dt,
                     split_every=split_every,
                     combine=partial(mean_combine, sum=chunk.nansum, numel=nannumel))
