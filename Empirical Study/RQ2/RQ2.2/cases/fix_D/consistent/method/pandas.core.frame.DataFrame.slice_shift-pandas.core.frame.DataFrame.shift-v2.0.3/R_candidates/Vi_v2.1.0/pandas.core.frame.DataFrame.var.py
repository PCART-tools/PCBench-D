    @doc(make_doc("var", ndim=2))
    def var(
        self,
        axis: Axis | None = 0,
        skipna: bool = True,
        ddof: int = 1,
        numeric_only: bool = False,
        **kwargs,
    ):
        result = super().var(axis, skipna, ddof, numeric_only, **kwargs)
        if isinstance(result, Series):
            result = result.__finalize__(self, method="var")
        return result
