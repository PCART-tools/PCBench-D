    def min(self, *args, **kwargs):
        nv.validate_window_func("min", args, kwargs)
        window_func = self._get_cython_func_type("roll_min")
        return self._apply(window_func, center=self.center, name="min", **kwargs)
