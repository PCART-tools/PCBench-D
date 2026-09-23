    def max(self, *args, **kwargs):
        nv.validate_window_func("max", args, kwargs)
        window_func = self._get_cython_func_type("roll_max")
        return self._apply(window_func, center=self.center, name="max", **kwargs)
