    @wraps(np.max)
    def max(self, axis=None, keepdims=False, split_every=None, out=None):
        from .reductions import max
        return max(self, axis=axis, keepdims=keepdims, split_every=split_every,
                   out=out)
