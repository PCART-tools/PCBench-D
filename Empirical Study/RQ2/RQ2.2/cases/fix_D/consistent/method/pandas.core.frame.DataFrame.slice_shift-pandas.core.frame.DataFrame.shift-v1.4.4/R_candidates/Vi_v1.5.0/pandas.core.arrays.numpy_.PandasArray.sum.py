    def sum(
        self, *, axis: int | None = None, skipna: bool = True, min_count=0, **kwargs
    ) -> Scalar:
        nv.validate_sum((), kwargs)
        result = nanops.nansum(
            self._ndarray, axis=axis, skipna=skipna, min_count=min_count
        )
        return self._wrap_reduction_result(axis, result)
