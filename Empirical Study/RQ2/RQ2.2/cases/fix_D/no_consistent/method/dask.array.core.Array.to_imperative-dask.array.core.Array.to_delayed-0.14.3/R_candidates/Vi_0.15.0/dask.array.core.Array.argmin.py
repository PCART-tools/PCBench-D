    @wraps(np.argmin)
    def argmin(self, axis=None, split_every=None, out=None):
        from .reductions import argmin
        return argmin(self, axis=axis, split_every=split_every, out=out)
