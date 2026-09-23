    def quantile(
        self,
        q: float,
        interpolation: QuantileInterpolation = "linear",
        numeric_only: bool = False,
    ):
        if q == 1.0:
            window_func = window_aggregations.roll_max
        elif q == 0.0:
            window_func = window_aggregations.roll_min
        else:
            window_func = partial(
                window_aggregations.roll_quantile,
                quantile=q,
                interpolation=interpolation,
            )

        return self._apply(window_func, name="quantile", numeric_only=numeric_only)
