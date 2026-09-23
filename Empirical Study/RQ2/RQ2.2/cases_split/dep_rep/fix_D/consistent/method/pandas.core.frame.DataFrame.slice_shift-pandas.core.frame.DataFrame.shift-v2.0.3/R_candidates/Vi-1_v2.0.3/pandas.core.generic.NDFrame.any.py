    def any(
        self,
        axis: Axis = 0,
        bool_only: bool_t = False,
        skipna: bool_t = True,
        **kwargs,
    ) -> DataFrame | Series | bool_t:
        return self._logical_func(
            "any", nanops.nanany, axis, bool_only, skipna, **kwargs
        )
