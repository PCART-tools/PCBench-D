    def min(
        self, *, axis: AxisInt | None = None, skipna: bool = True, **kwargs
    ) -> Scalar:
        nv.validate_min((), kwargs)
        result = nanops.nanmin(
            values=self._ndarray, axis=axis, mask=self.isna(), skipna=skipna
        )
        return self._wrap_reduction_result(axis, result)
