    @wraps(np.mean)
    def mean(self, axis=None, dtype=None, keepdims=False, split_every=None):
        from .reductions import mean
        return mean(self, axis=axis, dtype=dtype, keepdims=keepdims,
                    split_every=split_every)
