    def min(self, axis=None, out=None, keepdims=False, skipna=True):
        nv.validate_min((), dict(out=out, keepdims=keepdims))
        return nanops.nanmin(self._ndarray, axis=axis, skipna=skipna)
