    @doc(make_doc("kurt", ndim=2))
    def kurt(
        self,
        axis: Axis | None = 0,
        skipna: bool = True,
        numeric_only: bool = False,
        **kwargs,
    ):
        result = super().kurt(axis, skipna, numeric_only, **kwargs)
        if isinstance(result, Series):
            result = result.__finalize__(self, method="kurt")
        return result
