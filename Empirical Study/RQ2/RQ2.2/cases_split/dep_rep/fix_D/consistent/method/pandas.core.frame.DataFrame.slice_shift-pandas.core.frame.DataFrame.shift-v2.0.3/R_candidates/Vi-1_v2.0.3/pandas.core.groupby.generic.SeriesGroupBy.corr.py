    @doc(Series.corr.__doc__)
    def corr(
        self,
        other: Series,
        method: CorrelationMethod = "pearson",
        min_periods: int | None = None,
    ) -> Series:
        result = self._op_via_apply(
            "corr", other=other, method=method, min_periods=min_periods
        )
        return result
