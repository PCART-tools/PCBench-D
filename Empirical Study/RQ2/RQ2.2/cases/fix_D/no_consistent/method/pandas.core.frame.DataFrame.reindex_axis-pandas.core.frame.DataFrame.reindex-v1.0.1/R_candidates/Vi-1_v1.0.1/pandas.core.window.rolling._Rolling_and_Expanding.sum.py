    def sum(self, *args, **kwargs):
        nv.validate_window_func("sum", args, kwargs)
        window_func = self._get_cython_func_type("roll_sum")
        kwargs.pop("floor", None)
        return self._apply(
            window_func, center=self.center, floor=0, name="sum", **kwargs
        )
