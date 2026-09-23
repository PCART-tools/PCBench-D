    def mean(self, axis=None, dtype=None, out=None, keepdims=False,
             skipna=True):
        nv.validate_mean((), dict(dtype=dtype, out=out, keepdims=keepdims))
        return nanops.nanmean(self._ndarray, axis=axis, skipna=skipna)
