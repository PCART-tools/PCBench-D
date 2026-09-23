    def skew(self, **kwargs):
        return self._apply(
            "roll_skew", "skew", check_minp=_require_min_periods(3), **kwargs
        )
