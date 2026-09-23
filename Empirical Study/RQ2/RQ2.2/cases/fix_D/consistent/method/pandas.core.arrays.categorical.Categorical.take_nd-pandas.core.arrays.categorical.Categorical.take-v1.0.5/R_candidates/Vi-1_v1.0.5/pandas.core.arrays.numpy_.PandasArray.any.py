    def any(self, axis=None, out=None, keepdims=False, skipna=True):
        nv.validate_any((), dict(out=out, keepdims=keepdims))
        return nanops.nanany(self._ndarray, axis=axis, skipna=skipna)
