    def all(
        self,
        axis: Axis = 0,
        bool_only: bool_t | None = None,
        skipna: bool_t = True,
        level: Level | None = None,
        **kwargs,
    ) -> Series | bool_t:
        return self._logical_func(
            "all", nanops.nanall, axis, bool_only, skipna, level, **kwargs
        )
