def nanstd(a, axis=None, dtype=None, keepdims=False, ddof=0, split_every=None):
    result = sqrt(nanvar(a, axis=axis, dtype=dtype, keepdims=keepdims,
                         ddof=ddof, split_every=split_every))
    if dtype and dtype != result.dtype:
        result = result.astype(dtype)
    return result
