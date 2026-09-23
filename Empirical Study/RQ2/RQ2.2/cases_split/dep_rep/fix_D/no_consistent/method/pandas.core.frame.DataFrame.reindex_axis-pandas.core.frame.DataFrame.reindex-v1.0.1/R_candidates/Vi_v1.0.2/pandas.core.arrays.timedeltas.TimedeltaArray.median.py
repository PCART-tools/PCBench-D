    def median(
        self,
        axis=None,
        out=None,
        overwrite_input: bool = False,
        keepdims: bool = False,
        skipna: bool = True,
    ):
        nv.validate_median(
            (), dict(out=out, overwrite_input=overwrite_input, keepdims=keepdims)
        )
        return nanops.nanmedian(self._data, axis=axis, skipna=skipna)
