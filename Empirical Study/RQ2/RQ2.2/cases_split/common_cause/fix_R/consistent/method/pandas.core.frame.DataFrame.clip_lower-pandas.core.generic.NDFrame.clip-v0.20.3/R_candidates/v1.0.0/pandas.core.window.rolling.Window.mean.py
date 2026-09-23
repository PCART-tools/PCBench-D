    @Substitution(name="window")
    @Appender(_shared_docs["mean"])
    def mean(self, *args, **kwargs):
        nv.validate_window_func("mean", args, kwargs)
        window_func = self._get_roll_func("roll_weighted_mean")
        window_func = get_weighted_roll_func(window_func)
        return self._apply(
            window_func, center=self.center, is_weighted=True, name="mean", **kwargs
        )
