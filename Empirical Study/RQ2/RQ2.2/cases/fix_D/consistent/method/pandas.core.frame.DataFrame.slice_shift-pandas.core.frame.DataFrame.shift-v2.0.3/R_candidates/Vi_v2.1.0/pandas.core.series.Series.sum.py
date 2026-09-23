    @doc(make_doc("sum", ndim=1))
    def sum(
        self,
        axis: Axis | None = None,
        skipna: bool = True,
        numeric_only: bool = False,
        min_count: int = 0,
        **kwargs,
    ):
        return NDFrame.sum(self, axis, skipna, numeric_only, min_count, **kwargs)
