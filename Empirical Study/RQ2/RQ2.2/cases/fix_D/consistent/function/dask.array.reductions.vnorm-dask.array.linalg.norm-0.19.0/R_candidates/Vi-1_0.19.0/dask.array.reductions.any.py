@wraps(chunk.any)
def any(a, axis=None, keepdims=False, split_every=None, out=None):
    return reduction(a, chunk.any, chunk.any, axis=axis, keepdims=keepdims,
                     dtype='bool', split_every=split_every, out=out)
