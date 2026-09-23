    @doc(DataFrame.cov.__doc__)
    def cov(
        self,
        min_periods: int | None = None,
        ddof: int | None = 1,
        numeric_only: bool = False,
    ) -> DataFrame:
        result = self._op_via_apply(
            "cov", min_periods=min_periods, ddof=ddof, numeric_only=numeric_only
        )
        return result
