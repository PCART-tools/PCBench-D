    @doc(make_doc("prod", ndim=2))
    def prod(
        self,
        axis: Axis | None = 0,
        skipna: bool = True,
        numeric_only: bool = False,
        min_count: int = 0,
        **kwargs,
    ):
        result = super().prod(axis, skipna, numeric_only, min_count, **kwargs)
        return result.__finalize__(self, method="prod")
