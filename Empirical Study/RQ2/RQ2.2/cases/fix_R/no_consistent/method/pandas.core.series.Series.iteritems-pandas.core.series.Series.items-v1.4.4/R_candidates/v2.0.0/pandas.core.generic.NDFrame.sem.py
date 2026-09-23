    def sem(
        self,
        axis: Axis | None = None,
        skipna: bool_t = True,
        ddof: int = 1,
        numeric_only: bool_t = False,
        **kwargs,
    ) -> Series | float:
        return self._stat_function_ddof(
            "sem", nanops.nansem, axis, skipna, ddof, numeric_only, **kwargs
        )
