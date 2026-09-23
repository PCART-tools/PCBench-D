    def max(
        self,
        axis: Axis | None | lib.NoDefault = lib.no_default,
        skipna: bool_t = True,
        level: Level | None = None,
        numeric_only: bool_t | None = None,
        **kwargs,
    ):
        return self._stat_function(
            "max",
            nanops.nanmax,
            axis,
            skipna,
            level,
            numeric_only,
            **kwargs,
        )
