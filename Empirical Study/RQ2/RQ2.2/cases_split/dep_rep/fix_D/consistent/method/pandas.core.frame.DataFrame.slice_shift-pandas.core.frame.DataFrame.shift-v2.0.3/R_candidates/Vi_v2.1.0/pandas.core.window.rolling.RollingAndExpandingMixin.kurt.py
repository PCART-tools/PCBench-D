    def kurt(self, numeric_only: bool = False):
        window_func = window_aggregations.roll_kurt
        return self._apply(
            window_func,
            name="kurt",
            numeric_only=numeric_only,
        )
