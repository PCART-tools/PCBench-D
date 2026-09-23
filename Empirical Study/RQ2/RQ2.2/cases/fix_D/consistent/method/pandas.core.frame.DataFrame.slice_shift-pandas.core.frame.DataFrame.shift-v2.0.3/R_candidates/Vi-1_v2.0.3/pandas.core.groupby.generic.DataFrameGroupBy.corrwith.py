    @doc(DataFrame.corrwith.__doc__)
    def corrwith(
        self,
        other: DataFrame | Series,
        axis: Axis = 0,
        drop: bool = False,
        method: CorrelationMethod = "pearson",
        numeric_only: bool = False,
    ) -> DataFrame:
        result = self._op_via_apply(
            "corrwith",
            other=other,
            axis=axis,
            drop=drop,
            method=method,
            numeric_only=numeric_only,
        )
        return result
