    def skew(
        self,
        axis: Axis | None | lib.NoDefault = lib.no_default,
        skipna: bool_t = True,
        level: Level | None = None,
        numeric_only: bool_t | None = None,
        **kwargs,
    ) -> Series | float:
        return self._stat_function(
            "skew", nanops.nanskew, axis, skipna, level, numeric_only, **kwargs
        )
