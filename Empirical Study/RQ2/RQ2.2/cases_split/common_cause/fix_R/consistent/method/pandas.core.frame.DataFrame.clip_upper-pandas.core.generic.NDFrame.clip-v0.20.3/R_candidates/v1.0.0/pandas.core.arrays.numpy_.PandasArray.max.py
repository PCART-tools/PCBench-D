    def max(self, axis=None, out=None, keepdims=False, skipna=True):
        nv.validate_max((), dict(out=out, keepdims=keepdims))
        return nanops.nanmax(self._ndarray, axis=axis, skipna=skipna)
