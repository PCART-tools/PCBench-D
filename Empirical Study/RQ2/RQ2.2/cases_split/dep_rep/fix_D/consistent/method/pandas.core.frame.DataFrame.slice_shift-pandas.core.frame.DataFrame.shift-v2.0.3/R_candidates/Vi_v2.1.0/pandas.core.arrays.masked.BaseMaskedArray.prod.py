    def prod(
        self,
        *,
        skipna: bool = True,
        min_count: int = 0,
        axis: AxisInt | None = 0,
        **kwargs,
    ):
        nv.validate_prod((), kwargs)

        result = masked_reductions.prod(
            self._data,
            self._mask,
            skipna=skipna,
            min_count=min_count,
            axis=axis,
        )
        return self._wrap_min_count_reduction_result(
            "prod", result, skipna=skipna, min_count=min_count, axis=axis
        )
