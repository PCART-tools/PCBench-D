    def count(self):
        window_func = window_aggregations.roll_sum
        return self._apply(window_func, name="count")
