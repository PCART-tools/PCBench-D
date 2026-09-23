@wraps(chunk.min)
def min(a, axis=None, keepdims=False, split_every=None, out=None):
    return reduction(a, chunk.min, chunk.min, axis=axis, keepdims=keepdims,
                     dtype=a.dtype, split_every=split_every, out=out)
