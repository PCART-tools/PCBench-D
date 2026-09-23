    def var(
        self,
        axis: Axis | None = None,
        skipna: bool_t = True,
        level: Level | None = None,
        ddof: int = 1,
        numeric_only: bool_t | None = None,
        **kwargs,
    ) -> Series | float:
        return self._stat_function_ddof(
            "var", nanops.nanvar, axis, skipna, level, ddof, numeric_only, **kwargs
        )
