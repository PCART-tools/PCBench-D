@wraps(chunk.mean)
def mean(a, axis=None, dtype=None, keepdims=False, split_every=None, out=None):
    if dtype is not None:
        dt = dtype
    else:
        dt = getattr(np.mean(np.empty(shape=(1,), dtype=a.dtype)), 'dtype', object)
    return reduction(a, mean_chunk, mean_agg, axis=axis, keepdims=keepdims,
                     dtype=dt, split_every=split_every, combine=mean_combine,
                     out=out)
