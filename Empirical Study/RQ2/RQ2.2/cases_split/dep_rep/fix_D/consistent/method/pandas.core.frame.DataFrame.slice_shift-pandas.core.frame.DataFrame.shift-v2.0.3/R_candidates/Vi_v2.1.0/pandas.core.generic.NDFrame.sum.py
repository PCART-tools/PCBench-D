    def sum(
        self,
        axis: Axis | None = 0,
        skipna: bool_t = True,
        numeric_only: bool_t = False,
        min_count: int = 0,
        **kwargs,
    ):
        return self._min_count_stat_function(
            "sum", nanops.nansum, axis, skipna, numeric_only, min_count, **kwargs
        )
