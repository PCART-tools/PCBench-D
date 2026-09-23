    @doc(make_doc("mean", ndim=2))
    def mean(
        self,
        axis: Axis | None = 0,
        skipna: bool = True,
        numeric_only: bool = False,
        **kwargs,
    ):
        result = super().mean(axis, skipna, numeric_only, **kwargs)
        if isinstance(result, Series):
            result = result.__finalize__(self, method="mean")
        return result
