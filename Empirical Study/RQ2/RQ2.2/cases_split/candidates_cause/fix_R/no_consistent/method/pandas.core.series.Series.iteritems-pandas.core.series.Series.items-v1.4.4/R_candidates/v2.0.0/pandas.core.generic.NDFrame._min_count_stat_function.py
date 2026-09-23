    @final
    def _min_count_stat_function(
        self,
        name: str,
        func,
        axis: Axis | None = None,
        skipna: bool_t = True,
        numeric_only: bool_t = False,
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

        return self._reduce(
            func,
            name=name,
            axis=axis,
            skipna=skipna,
            numeric_only=numeric_only,
            min_count=min_count,
        )
