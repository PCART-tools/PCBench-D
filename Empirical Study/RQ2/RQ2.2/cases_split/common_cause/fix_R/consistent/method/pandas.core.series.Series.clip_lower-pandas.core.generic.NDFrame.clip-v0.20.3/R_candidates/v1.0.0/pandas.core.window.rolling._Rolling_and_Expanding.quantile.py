    def quantile(self, quantile, interpolation="linear", **kwargs):
        if quantile == 1.0:
            window_func = self._get_cython_func_type("roll_max")
        elif quantile == 0.0:
            window_func = self._get_cython_func_type("roll_min")
        else:
            window_func = partial(
                self._get_roll_func("roll_quantile"),
                win=self._get_window(),
                quantile=quantile,
                interpolation=interpolation,
            )

        # Pass through for groupby.rolling
        kwargs["quantile"] = quantile
        kwargs["interpolation"] = interpolation
        return self._apply(window_func, center=self.center, name="quantile", **kwargs)
