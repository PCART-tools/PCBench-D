    def kurt(self, **kwargs):
        window_func = window_aggregations.roll_kurt
        return self._apply(
            window_func,
            name="kurt",
            **kwargs,
        )
