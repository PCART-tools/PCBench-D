    def all(self, axis=None, out=None, keepdims=False, skipna=True):
        nv.validate_all((), dict(out=out, keepdims=keepdims))
        return nanops.nanall(self._ndarray, axis=axis, skipna=skipna)
