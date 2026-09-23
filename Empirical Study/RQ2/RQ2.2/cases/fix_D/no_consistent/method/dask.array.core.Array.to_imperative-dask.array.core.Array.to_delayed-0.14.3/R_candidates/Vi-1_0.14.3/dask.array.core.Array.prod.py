    @wraps(np.prod)
    def prod(self, axis=None, dtype=None, keepdims=False, split_every=None):
        from .reductions import prod
        return prod(self, axis=axis, dtype=dtype, keepdims=keepdims,
                    split_every=split_every)
