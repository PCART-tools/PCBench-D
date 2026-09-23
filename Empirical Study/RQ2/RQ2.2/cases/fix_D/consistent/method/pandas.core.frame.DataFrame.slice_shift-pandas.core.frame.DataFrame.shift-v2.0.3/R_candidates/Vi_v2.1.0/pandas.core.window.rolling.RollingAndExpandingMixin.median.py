    def median(
        self,
        numeric_only: bool = False,
        engine: Literal["cython", "numba"] | None = None,
        engine_kwargs: dict[str, bool] | None = None,
    ):
        if maybe_use_numba(engine):
            if self.method == "table":
                func = generate_manual_numpy_nan_agg_with_axis(np.nanmedian)
            else:
                func = np.nanmedian

            return self.apply(
                func,
                raw=True,
                engine=engine,
                engine_kwargs=engine_kwargs,
            )
        window_func = window_aggregations.roll_median_c
        return self._apply(window_func, name="median", numeric_only=numeric_only)
