    @wraps(np.all)
    def all(self, axis=None, keepdims=False, split_every=None):
        from .reductions import all
        return all(self, axis=axis, keepdims=keepdims, split_every=split_every)
