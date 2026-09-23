    def std(
        self,
        ddof: int = 1,
        numeric_only: bool = False,
        engine: Literal["cython", "numba"] | None = None,
        engine_kwargs: dict[str, bool] | None = None,
    ):
        if maybe_use_numba(engine):
            if self.method == "table":
                raise NotImplementedError("std not supported with method='table'")
            from pandas.core._numba.kernels import sliding_var

            return zsqrt(self._numba_apply(sliding_var, engine_kwargs, ddof=ddof))
        window_func = window_aggregations.roll_var

        def zsqrt_func(values, begin, end, min_periods):
            return zsqrt(window_func(values, begin, end, min_periods, ddof=ddof))

        return self._apply(
            zsqrt_func,
            name="std",
            numeric_only=numeric_only,
        )
