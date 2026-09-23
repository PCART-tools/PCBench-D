    @final
    def _stat_function_ddof(
        self,
        name: str,
        func,
        axis: Axis | None = None,
        skipna: bool_t = True,
        ddof: int = 1,
        numeric_only: bool_t = False,
        **kwargs,
    ) -> Series | float:
        nv.validate_stat_ddof_func((), kwargs, fname=name)
        validate_bool_kwarg(skipna, "skipna", none_allowed=False)
        if axis is None:
            axis = self._stat_axis_number

        return self._reduce(
            func, name, axis=axis, numeric_only=numeric_only, skipna=skipna, ddof=ddof
        )
