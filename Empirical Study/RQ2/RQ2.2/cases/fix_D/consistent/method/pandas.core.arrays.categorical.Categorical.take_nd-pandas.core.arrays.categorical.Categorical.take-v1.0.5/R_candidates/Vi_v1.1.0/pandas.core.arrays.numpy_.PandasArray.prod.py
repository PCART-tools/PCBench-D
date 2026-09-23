    def prod(self, axis=None, skipna=True, min_count=0, **kwargs) -> Scalar:
        nv.validate_prod((), kwargs)
        return nanops.nanprod(
            self._ndarray, axis=axis, skipna=skipna, min_count=min_count
        )
