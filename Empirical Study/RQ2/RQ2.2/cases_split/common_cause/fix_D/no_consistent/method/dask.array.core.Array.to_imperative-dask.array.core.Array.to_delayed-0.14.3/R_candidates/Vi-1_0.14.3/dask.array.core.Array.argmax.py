    @wraps(np.argmax)
    def argmax(self, axis=None, split_every=None):
        from .reductions import argmax
        return argmax(self, axis=axis, split_every=split_every)
