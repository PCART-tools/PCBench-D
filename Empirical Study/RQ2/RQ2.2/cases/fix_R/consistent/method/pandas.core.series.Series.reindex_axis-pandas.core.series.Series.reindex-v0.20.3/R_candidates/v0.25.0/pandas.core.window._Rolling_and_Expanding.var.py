    def var(self, ddof=1, *args, **kwargs):
        nv.validate_window_func("var", args, kwargs)
        return self._apply(
            "roll_var", "var", check_minp=_require_min_periods(1), ddof=ddof, **kwargs
        )
