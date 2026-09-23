    def sum(self, axis=None, skipna=True, min_count=0, **kwargs) -> Scalar:
        nv.validate_sum((), kwargs)
        return nanops.nansum(
            self._ndarray, axis=axis, skipna=skipna, min_count=min_count
        )
