    def min(self, *, skipna: bool = True, axis: AxisInt | None = 0, **kwargs):
        nv.validate_min((), kwargs)
        result = masked_reductions.min(
            self._data,
            self._mask,
            skipna=skipna,
            axis=axis,
        )
        return self._wrap_reduction_result("min", result, skipna=skipna, axis=axis)
