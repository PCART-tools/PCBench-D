@wraps(chunk.max)
def max(a, axis=None, keepdims=False, split_every=None):
    return reduction(a, chunk.max, chunk.max, axis=axis, keepdims=keepdims,
                     dtype=a.dtype, split_every=split_every)
