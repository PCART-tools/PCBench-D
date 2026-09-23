    def mean(self, *, skipna: bool = True, axis: AxisInt | None = 0, **kwargs):
        nv.validate_mean((), kwargs)
        result = masked_reductions.mean(
            self._data,
            self._mask,
            skipna=skipna,
            axis=axis,
        )
        return self._wrap_reduction_result(
            "mean", result, skipna=skipna, axis=axis, **kwargs
        )
