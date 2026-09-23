    @wraps(np.any)
    def any(self, axis=None, keepdims=False, split_every=None, out=None):
        from .reductions import any
        return any(self, axis=axis, keepdims=keepdims, split_every=split_every,
                   out=out)
