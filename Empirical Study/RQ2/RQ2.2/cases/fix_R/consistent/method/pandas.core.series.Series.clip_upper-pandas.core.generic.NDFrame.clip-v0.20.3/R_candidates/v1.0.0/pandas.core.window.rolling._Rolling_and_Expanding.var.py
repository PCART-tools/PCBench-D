    def var(self, ddof=1, *args, **kwargs):
        nv.validate_window_func("var", args, kwargs)
        kwargs.pop("require_min_periods", None)
        window_func = partial(self._get_cython_func_type("roll_var"), ddof=ddof)
        # ddof passed again for compat with groupby.rolling
        return self._apply(
            window_func,
            center=self.center,
            require_min_periods=1,
            name="var",
            ddof=ddof,
            **kwargs,
        )
