    @wraps(np.sum)
    def sum(self, axis=None, dtype=None, keepdims=False, split_every=None,
            out=None):
        from .reductions import sum
        return sum(self, axis=axis, dtype=dtype, keepdims=keepdims,
                   split_every=split_every, out=out)
