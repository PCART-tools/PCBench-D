    def std(self, ddof=1, *args, **kwargs):
        nv.validate_window_func("std", args, kwargs)
        window = self._get_window()
        index_as_array = self._get_index()

        def f(arg, *args, **kwargs):
            minp = _require_min_periods(1)(self.min_periods, window)
            return _zsqrt(
                libwindow.roll_var(arg, window, minp, index_as_array, self.closed, ddof)
            )

        return self._apply(
            f, "std", check_minp=_require_min_periods(1), ddof=ddof, **kwargs
        )
