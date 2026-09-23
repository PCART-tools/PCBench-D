@wraps(chunk.all)
def all(a, axis=None, keepdims=False, split_every=None):
    return reduction(a, chunk.all, chunk.all, axis=axis, keepdims=keepdims,
                     dtype='bool', split_every=split_every)
