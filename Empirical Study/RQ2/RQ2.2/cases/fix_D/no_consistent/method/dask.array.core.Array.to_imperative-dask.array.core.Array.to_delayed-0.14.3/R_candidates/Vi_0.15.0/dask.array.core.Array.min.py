    @wraps(np.min)
    def min(self, axis=None, keepdims=False, split_every=None, out=None):
        from .reductions import min
        return min(self, axis=axis, keepdims=keepdims, split_every=split_every,
                   out=out)
