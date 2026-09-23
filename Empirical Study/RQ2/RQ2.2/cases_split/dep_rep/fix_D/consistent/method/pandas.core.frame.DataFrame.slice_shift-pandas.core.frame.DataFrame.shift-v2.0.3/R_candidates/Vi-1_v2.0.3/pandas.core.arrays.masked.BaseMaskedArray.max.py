    def max(self, *, skipna: bool = True, axis: AxisInt | None = 0, **kwargs):
        nv.validate_max((), kwargs)
        return masked_reductions.max(
            self._data,
            self._mask,
            skipna=skipna,
            axis=axis,
        )
