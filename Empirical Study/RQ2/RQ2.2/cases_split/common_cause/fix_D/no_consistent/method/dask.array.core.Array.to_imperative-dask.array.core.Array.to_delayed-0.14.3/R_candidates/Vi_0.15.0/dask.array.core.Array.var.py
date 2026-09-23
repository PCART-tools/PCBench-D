    @wraps(np.var)
    def var(self, axis=None, dtype=None, keepdims=False, ddof=0,
            split_every=None, out=None):
        from .reductions import var
        return var(self, axis=axis, dtype=dtype, keepdims=keepdims, ddof=ddof,
                   split_every=split_every, out=out)
