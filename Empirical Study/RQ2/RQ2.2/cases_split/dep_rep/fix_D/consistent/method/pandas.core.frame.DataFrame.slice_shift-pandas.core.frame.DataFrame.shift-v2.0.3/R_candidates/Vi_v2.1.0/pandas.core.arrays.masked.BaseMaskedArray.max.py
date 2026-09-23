    def max(self, *, skipna: bool = True, axis: AxisInt | None = 0, **kwargs):
        nv.validate_max((), kwargs)
        result = masked_reductions.max(
            self._data,
            self._mask,
            skipna=skipna,
            axis=axis,
        )
        return self._wrap_reduction_result("max", result, skipna=skipna, axis=axis)
