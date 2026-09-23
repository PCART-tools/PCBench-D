    @doc(make_doc("max", ndim=2))
    def max(
        self,
        axis: Axis | None = 0,
        skipna: bool = True,
        numeric_only: bool = False,
        **kwargs,
    ):
        result = super().max(axis, skipna, numeric_only, **kwargs)
        if isinstance(result, Series):
            result = result.__finalize__(self, method="max")
        return result
