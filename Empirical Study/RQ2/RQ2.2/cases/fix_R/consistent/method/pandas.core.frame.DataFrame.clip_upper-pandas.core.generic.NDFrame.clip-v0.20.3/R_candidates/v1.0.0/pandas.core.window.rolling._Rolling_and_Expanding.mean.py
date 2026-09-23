    def mean(self, *args, **kwargs):
        nv.validate_window_func("mean", args, kwargs)
        window_func = self._get_cython_func_type("roll_mean")
        return self._apply(window_func, center=self.center, name="mean", **kwargs)
