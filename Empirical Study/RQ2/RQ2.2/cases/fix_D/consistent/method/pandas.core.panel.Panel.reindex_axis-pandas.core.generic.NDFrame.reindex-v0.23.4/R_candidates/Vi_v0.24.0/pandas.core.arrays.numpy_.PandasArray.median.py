    def median(self, axis=None, out=None, overwrite_input=False,
               keepdims=False, skipna=True):
        nv.validate_median((), dict(out=out, overwrite_input=overwrite_input,
                                    keepdims=keepdims))
        return nanops.nanmedian(self._ndarray, axis=axis, skipna=skipna)
