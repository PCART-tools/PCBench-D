    def median(
        self,
        axis: Axis | None = 0,
        skipna: bool_t = True,
        numeric_only: bool_t = False,
        **kwargs,
    ) -> Series | float:
        return self._stat_function(
            "median", nanops.nanmedian, axis, skipna, numeric_only, **kwargs
        )
