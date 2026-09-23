    def min(self, *args, **kwargs):
        nv.validate_window_func("min", args, kwargs)
        return self._apply("roll_min", "min", **kwargs)
