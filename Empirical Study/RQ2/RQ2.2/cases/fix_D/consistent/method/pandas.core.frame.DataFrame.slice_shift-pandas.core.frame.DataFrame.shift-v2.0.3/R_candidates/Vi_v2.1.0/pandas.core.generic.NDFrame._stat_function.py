    @final
    def _stat_function(
        self,
        name: str,
        func,
        axis: Axis | None = 0,
        skipna: bool_t = True,
        numeric_only: bool_t = False,
        **kwargs,
    ):
        assert name in ["median", "mean", "min", "max", "kurt", "skew"], name
        nv.validate_func(name, (), kwargs)

        validate_bool_kwarg(skipna, "skipna", none_allowed=False)

        return self._reduce(
            func, name=name, axis=axis, skipna=skipna, numeric_only=numeric_only
        )
