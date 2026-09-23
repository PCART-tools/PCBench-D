    def median(self, *, axis: int | None = None, skipna: bool = True, **kwargs):
        nv.validate_median((), kwargs)

        if axis is not None and abs(axis) >= self.ndim:
            raise ValueError("abs(axis) must be less than ndim")

        if is_period_dtype(self.dtype):
            # pass datetime64 values to nanops to get correct NaT semantics
            result = nanops.nanmedian(
                self._ndarray.view("M8[ns]"), axis=axis, skipna=skipna
            )
            result = result.view("i8")
            if axis is None or self.ndim == 1:
                return self._box_func(result)
            return self._from_backing_data(result)

        result = nanops.nanmedian(self._ndarray, axis=axis, skipna=skipna)
        return self._wrap_reduction_result(axis, result)
