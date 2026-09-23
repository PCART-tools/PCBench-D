    def prod(
        self,
        axis: Axis | None = None,
        skipna: bool_t = True,
        level: Level | None = None,
        numeric_only: bool_t | None = None,
        min_count: int = 0,
        **kwargs,
    ):
        return self._min_count_stat_function(
            "prod",
            nanops.nanprod,
            axis,
            skipna,
            level,
            numeric_only,
            min_count,
            **kwargs,
        )
