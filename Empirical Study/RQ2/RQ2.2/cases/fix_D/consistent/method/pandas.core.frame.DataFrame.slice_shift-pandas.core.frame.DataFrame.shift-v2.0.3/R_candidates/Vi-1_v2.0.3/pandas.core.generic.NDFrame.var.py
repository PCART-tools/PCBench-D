    def var(
        self,
        axis: Axis | None = None,
        skipna: bool_t = True,
        ddof: int = 1,
        numeric_only: bool_t = False,
        **kwargs,
    ) -> Series | float:
        return self._stat_function_ddof(
            "var", nanops.nanvar, axis, skipna, ddof, numeric_only, **kwargs
        )
