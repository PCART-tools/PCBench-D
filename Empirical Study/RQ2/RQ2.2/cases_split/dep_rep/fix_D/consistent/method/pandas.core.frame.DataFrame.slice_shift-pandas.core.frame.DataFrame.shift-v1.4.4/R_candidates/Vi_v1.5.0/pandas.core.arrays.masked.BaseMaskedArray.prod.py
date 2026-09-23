    def prod(self, *, skipna=True, min_count=0, axis: int | None = 0, **kwargs):
        nv.validate_prod((), kwargs)
        result = masked_reductions.prod(
            self._data,
            self._mask,
            skipna=skipna,
            min_count=min_count,
            axis=axis,
        )
        return self._wrap_reduction_result(
            "prod", result, skipna=skipna, axis=axis, **kwargs
        )
