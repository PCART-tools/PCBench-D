@wraps(chunk.nanmax)
def nanmax(a, axis=None, keepdims=False, split_every=None):
    return reduction(a, chunk.nanmax, chunk.nanmax, axis=axis,
                     keepdims=keepdims, dtype=a._dtype, split_every=split_every)
