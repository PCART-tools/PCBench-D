    def max(
        self,
        axis: Axis | None = 0,
        skipna: bool_t = True,
        numeric_only: bool_t = False,
        **kwargs,
    ):
        return self._stat_function(
            "max",
            nanops.nanmax,
            axis,
            skipna,
            numeric_only,
            **kwargs,
        )
