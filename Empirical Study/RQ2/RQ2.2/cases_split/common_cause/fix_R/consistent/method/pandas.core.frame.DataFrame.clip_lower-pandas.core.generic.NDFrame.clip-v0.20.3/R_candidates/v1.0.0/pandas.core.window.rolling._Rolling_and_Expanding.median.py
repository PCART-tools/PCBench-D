    def median(self, **kwargs):
        window_func = self._get_roll_func("roll_median_c")
        window_func = partial(window_func, win=self._get_window())
        return self._apply(window_func, center=self.center, name="median", **kwargs)
