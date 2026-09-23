    def min(self, *, skipna=True, axis: int | None = 0, **kwargs):
        nv.validate_min((), kwargs)
        return masked_reductions.min(
            self._data,
            self._mask,
            skipna=skipna,
            axis=axis,
        )
