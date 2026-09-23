    def skew(self, **kwargs):
        window_func = self._get_cython_func_type("roll_skew")
        kwargs.pop("require_min_periods", None)
        return self._apply(
            window_func,
            center=self.center,
            require_min_periods=3,
            name="skew",
            **kwargs,
        )
