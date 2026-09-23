    def quantile(self, quantile: float, interpolation: str = "linear", **kwargs):
        if quantile == 1.0:
            window_func = window_aggregations.roll_max
        elif quantile == 0.0:
            window_func = window_aggregations.roll_min
        else:
            window_func = partial(
                window_aggregations.roll_quantile,
                quantile=quantile,
                interpolation=interpolation,
            )

        return self._apply(window_func, name="quantile", **kwargs)
