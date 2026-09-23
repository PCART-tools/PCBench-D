    def sum(self, *args, **kwargs):
        nv.validate_window_func("sum", args, kwargs)
        return self._apply("roll_sum", "sum", **kwargs)
