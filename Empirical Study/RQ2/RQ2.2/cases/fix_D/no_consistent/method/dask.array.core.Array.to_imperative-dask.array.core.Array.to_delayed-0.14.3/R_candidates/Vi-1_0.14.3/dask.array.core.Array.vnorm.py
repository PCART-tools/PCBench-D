    def vnorm(self, ord=None, axis=None, keepdims=False, split_every=None):
        """ Vector norm """
        from .reductions import vnorm
        return vnorm(self, ord=ord, axis=axis, keepdims=keepdims,
                     split_every=split_every)
