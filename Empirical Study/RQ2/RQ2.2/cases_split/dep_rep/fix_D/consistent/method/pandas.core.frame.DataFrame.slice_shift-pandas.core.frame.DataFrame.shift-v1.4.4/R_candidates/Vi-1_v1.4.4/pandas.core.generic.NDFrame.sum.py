    def sum(
        self,
        axis: Axis | None = None,
        skipna: bool_t = True,
        level: Level | None = None,
        numeric_only: bool_t | None = None,
        min_count=0,
        **kwargs,
    ):
        return self._min_count_stat_function(
            "sum", nanops.nansum, axis, skipna, level, numeric_only, min_count, **kwargs
        )
