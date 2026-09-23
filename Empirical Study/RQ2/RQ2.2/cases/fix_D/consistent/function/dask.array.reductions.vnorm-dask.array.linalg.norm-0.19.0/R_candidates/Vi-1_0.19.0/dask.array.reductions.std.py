@wraps(chunk.std)
def std(a, axis=None, dtype=None, keepdims=False, ddof=0, split_every=None,
        out=None):
    result = sqrt(a.var(axis=axis, dtype=dtype, keepdims=keepdims, ddof=ddof,
                        split_every=split_every, out=out))
    if dtype and dtype != result.dtype:
        result = result.astype(dtype)
    return result
