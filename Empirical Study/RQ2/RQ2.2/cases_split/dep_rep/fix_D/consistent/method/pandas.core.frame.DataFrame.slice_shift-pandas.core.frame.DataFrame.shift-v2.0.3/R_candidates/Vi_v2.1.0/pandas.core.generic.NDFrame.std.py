    def std(
        self,
        axis: Axis | None = 0,
        skipna: bool_t = True,
        ddof: int = 1,
        numeric_only: bool_t = False,
        **kwargs,
    ) -> Series | float:
        return self._stat_function_ddof(
            "std", nanops.nanstd, axis, skipna, ddof, numeric_only, **kwargs
        )
