def nanmean(a, axis=None, dtype=None, keepdims=False, split_every=None):
    if dtype is not None:
        dt = dtype
    else:
        dt = np.mean(np.empty(shape=(1,), dtype=a.dtype)).dtype
    return reduction(a, partial(mean_chunk, sum=chunk.nansum, numel=nannumel),
                     mean_agg, axis=axis, keepdims=keepdims, dtype=dt,
                     split_every=split_every,
                     combine=partial(mean_combine, sum=chunk.nansum, numel=nannumel))
