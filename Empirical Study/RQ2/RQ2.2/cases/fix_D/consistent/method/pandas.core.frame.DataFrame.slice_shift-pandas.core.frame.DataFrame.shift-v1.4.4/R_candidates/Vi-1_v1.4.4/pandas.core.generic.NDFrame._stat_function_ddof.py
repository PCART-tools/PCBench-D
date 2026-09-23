    @final
    def _stat_function_ddof(
        self,
        name: str,
        func,
        axis: Axis | None = None,
        skipna: bool_t = True,
        level: Level | None = None,
        ddof: int = 1,
        numeric_only: bool_t | None = None,
        **kwargs,
    ) -> Series | float:
        nv.validate_stat_ddof_func((), kwargs, fname=name)
        validate_bool_kwarg(skipna, "skipna", none_allowed=False)
        if axis is None:
            axis = self._stat_axis_number
        if level is not None:
            warnings.warn(
                "Using the level keyword in DataFrame and Series aggregations is "
                "deprecated and will be removed in a future version. Use groupby "
                "instead. df.var(level=1) should use df.groupby(level=1).var().",
                FutureWarning,
                stacklevel=find_stack_level(),
            )
            return self._agg_by_level(
                name, axis=axis, level=level, skipna=skipna, ddof=ddof
            )
        return self._reduce(
            func, name, axis=axis, numeric_only=numeric_only, skipna=skipna, ddof=ddof
        )
