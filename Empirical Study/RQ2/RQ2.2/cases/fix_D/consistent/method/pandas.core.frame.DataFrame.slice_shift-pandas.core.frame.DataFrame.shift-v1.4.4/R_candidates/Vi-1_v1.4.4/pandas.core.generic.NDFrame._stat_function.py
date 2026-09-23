    @final
    def _stat_function(
        self,
        name: str,
        func,
        axis: Axis | None | lib.NoDefault = None,
        skipna: bool_t = True,
        level: Level | None = None,
        numeric_only: bool_t | None = None,
        **kwargs,
    ):
        if name == "median":
            nv.validate_median((), kwargs)
        else:
            nv.validate_stat_func((), kwargs, fname=name)

        validate_bool_kwarg(skipna, "skipna", none_allowed=False)

        if axis is None and level is None and self.ndim > 1:
            # user must have explicitly passed axis=None
            # GH#21597
            warnings.warn(
                f"In a future version, DataFrame.{name}(axis=None) will return a "
                f"scalar {name} over the entire DataFrame. To retain the old "
                f"behavior, use 'frame.{name}(axis=0)' or just 'frame.{name}()'",
                FutureWarning,
                stacklevel=find_stack_level(),
            )
        if axis is lib.no_default:
            axis = None

        if axis is None:
            axis = self._stat_axis_number
        axis = cast(Axis, axis)
        if level is not None:
            warnings.warn(
                "Using the level keyword in DataFrame and Series aggregations is "
                "deprecated and will be removed in a future version. Use groupby "
                "instead. df.median(level=1) should use df.groupby(level=1).median().",
                FutureWarning,
                stacklevel=find_stack_level(),
            )
            return self._agg_by_level(
                name, axis=axis, level=level, skipna=skipna, numeric_only=numeric_only
            )
        return self._reduce(
            func, name=name, axis=axis, skipna=skipna, numeric_only=numeric_only
        )
