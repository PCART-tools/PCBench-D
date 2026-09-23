    @final
    def _stat_function_ddof(
        self,
        name: str,
        func,
        axis: Axis | None | lib.NoDefault = lib.no_default,
        skipna: bool_t = True,
        ddof: int = 1,
        numeric_only: bool_t = False,
        **kwargs,
    ) -> Series | float:
        nv.validate_stat_ddof_func((), kwargs, fname=name)
        validate_bool_kwarg(skipna, "skipna", none_allowed=False)

        if axis is None:
            if self.ndim > 1:
                warnings.warn(
                    f"The behavior of {type(self).__name__}.{name} with axis=None "
                    "is deprecated, in a future version this will reduce over both "
                    "axes and return a scalar. To retain the old behavior, pass "
                    "axis=0 (or do not pass axis)",
                    FutureWarning,
                    stacklevel=find_stack_level(),
                )
            axis = 0
        elif axis is lib.no_default:
            axis = 0

        return self._reduce(
            func, name, axis=axis, numeric_only=numeric_only, skipna=skipna, ddof=ddof
        )
