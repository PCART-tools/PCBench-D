    def skew(self, **kwargs):
        window_func = window_aggregations.roll_skew
        return self._apply(
            window_func,
            name="skew",
            **kwargs,
        )
