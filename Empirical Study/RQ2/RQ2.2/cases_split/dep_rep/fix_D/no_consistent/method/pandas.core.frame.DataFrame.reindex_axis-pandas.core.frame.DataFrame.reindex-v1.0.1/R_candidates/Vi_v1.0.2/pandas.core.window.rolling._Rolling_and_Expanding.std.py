    def std(self, ddof=1, *args, **kwargs):
        nv.validate_window_func("std", args, kwargs)
        kwargs.pop("require_min_periods", None)
        window_func = self._get_cython_func_type("roll_var")

        def zsqrt_func(values, begin, end, min_periods):
            return zsqrt(window_func(values, begin, end, min_periods, ddof=ddof))

        # ddof passed again for compat with groupby.rolling
        return self._apply(
            zsqrt_func,
            center=self.center,
            require_min_periods=1,
            name="std",
            ddof=ddof,
            **kwargs,
        )
