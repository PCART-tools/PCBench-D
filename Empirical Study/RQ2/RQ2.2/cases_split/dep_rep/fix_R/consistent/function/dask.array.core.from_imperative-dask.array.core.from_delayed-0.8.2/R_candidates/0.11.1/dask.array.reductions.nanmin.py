@wraps(chunk.nanmin)
def nanmin(a, axis=None, keepdims=False, split_every=None):
    return reduction(a, chunk.nanmin, chunk.nanmin, axis=axis,
                     keepdims=keepdims, dtype=a._dtype, split_every=split_every)
