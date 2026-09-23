    @wraps(np.std)
    def std(self, axis=None, dtype=None, keepdims=False, ddof=0, split_every=None):
        from .reductions import std
        return std(self, axis=axis, dtype=dtype, keepdims=keepdims, ddof=ddof,
                   split_every=split_every)
