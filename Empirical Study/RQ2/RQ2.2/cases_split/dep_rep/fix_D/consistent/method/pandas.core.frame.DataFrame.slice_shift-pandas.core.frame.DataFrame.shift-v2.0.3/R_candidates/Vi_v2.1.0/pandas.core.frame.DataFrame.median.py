    @doc(make_doc("median", ndim=2))
    def median(
        self,
        axis: Axis | None = 0,
        skipna: bool = True,
        numeric_only: bool = False,
        **kwargs,
    ):
        result = super().median(axis, skipna, numeric_only, **kwargs)
        if isinstance(result, Series):
            result = result.__finalize__(self, method="median")
        return result
