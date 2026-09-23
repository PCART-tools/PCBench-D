    def prod(
        self,
        axis=None,
        dtype=None,
        out=None,
        keepdims=False,
        initial=None,
        skipna=True,
        min_count=0,
    ):
        nv.validate_prod(
            (), dict(dtype=dtype, out=out, keepdims=keepdims, initial=initial)
        )
        return nanops.nanprod(
            self._ndarray, axis=axis, skipna=skipna, min_count=min_count
        )
