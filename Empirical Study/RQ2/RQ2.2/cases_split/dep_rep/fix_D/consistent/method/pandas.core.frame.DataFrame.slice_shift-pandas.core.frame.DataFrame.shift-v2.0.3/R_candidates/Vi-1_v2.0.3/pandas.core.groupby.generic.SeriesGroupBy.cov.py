    @doc(Series.cov.__doc__)
    def cov(
        self, other: Series, min_periods: int | None = None, ddof: int | None = 1
    ) -> Series:
        result = self._op_via_apply(
            "cov", other=other, min_periods=min_periods, ddof=ddof
        )
        return result
