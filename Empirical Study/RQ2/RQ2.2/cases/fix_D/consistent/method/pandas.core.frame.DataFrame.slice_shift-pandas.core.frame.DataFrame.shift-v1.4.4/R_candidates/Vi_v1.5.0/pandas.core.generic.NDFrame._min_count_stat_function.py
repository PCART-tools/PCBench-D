    @final
    def _min_count_stat_function(
        self,
        name: str,
        func,
        axis: Axis | None = None,
        skipna: bool_t = True,
        level: Level | None = None,
        numeric_only: bool_t | None = None,
        min_count: int = 0,
        **kwargs,
    ):
        if name == "sum":
            nv.validate_sum((), kwargs)
        elif name == "prod":
            nv.validate_prod((), kwargs)
        else:
            nv.validate_stat_func((), kwargs, fname=name)

        validate_bool_kwarg(skipna, "skipna", none_allowed=False)

        if axis is None:
            axis = self._stat_axis_number
        if level is not None:
            warnings.warn(
                "Using the level keyword in DataFrame and Series aggregations is "
                "deprecated and will be removed in a future version. Use groupby "
                "instead. df.sum(level=1) should use df.groupby(level=1).sum().",
                FutureWarning,
                stacklevel=find_stack_level(inspect.currentframe()),
            )
            return self._agg_by_level(
                name,
                axis=axis,
                level=level,
                skipna=skipna,
                min_count=min_count,
                numeric_only=numeric_only,
            )

        return self._reduce(
            func,
            name=name,
            axis=axis,
            skipna=skipna,
            numeric_only=numeric_only,
            min_count=min_count,
        )
