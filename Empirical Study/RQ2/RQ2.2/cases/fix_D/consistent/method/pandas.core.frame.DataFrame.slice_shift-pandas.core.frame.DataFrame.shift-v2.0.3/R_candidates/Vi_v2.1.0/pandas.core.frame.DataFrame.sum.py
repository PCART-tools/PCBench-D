    @doc(make_doc("sum", ndim=2))
    def sum(
        self,
        axis: Axis | None = 0,
        skipna: bool = True,
        numeric_only: bool = False,
        min_count: int = 0,
        **kwargs,
    ):
        result = super().sum(axis, skipna, numeric_only, min_count, **kwargs)
        return result.__finalize__(self, method="sum")
