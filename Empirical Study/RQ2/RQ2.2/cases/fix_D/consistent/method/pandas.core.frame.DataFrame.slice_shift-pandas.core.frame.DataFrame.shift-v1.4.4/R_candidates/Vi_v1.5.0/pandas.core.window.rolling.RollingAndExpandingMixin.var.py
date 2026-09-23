    def var(
        self,
        ddof: int = 1,
        numeric_only: bool = False,
        *args,
        engine: str | None = None,
        engine_kwargs: dict[str, bool] | None = None,
        **kwargs,
    ):
        nv.validate_window_func("var", args, kwargs)
        if maybe_use_numba(engine):
            if self.method == "table":
                raise NotImplementedError("var not supported with method='table'")
            else:
                from pandas.core._numba.kernels import sliding_var

                return self._numba_apply(sliding_var, engine_kwargs, ddof)
        window_func = partial(window_aggregations.roll_var, ddof=ddof)
        return self._apply(
            window_func,
            name="var",
            numeric_only=numeric_only,
            **kwargs,
        )
