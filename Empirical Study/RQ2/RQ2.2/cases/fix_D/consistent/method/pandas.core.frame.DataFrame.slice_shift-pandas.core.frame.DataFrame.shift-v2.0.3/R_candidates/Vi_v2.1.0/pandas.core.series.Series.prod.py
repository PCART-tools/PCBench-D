    @doc(make_doc("prod", ndim=1))
    def prod(
        self,
        axis: Axis | None = None,
        skipna: bool = True,
        numeric_only: bool = False,
        min_count: int = 0,
        **kwargs,
    ):
        return NDFrame.prod(self, axis, skipna, numeric_only, min_count, **kwargs)
