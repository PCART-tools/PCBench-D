    @doc(make_doc("min", ndim=1))
    def min(
        self,
        axis: Axis | None = 0,
        skipna: bool = True,
        numeric_only: bool = False,
        **kwargs,
    ):
        return NDFrame.min(self, axis, skipna, numeric_only, **kwargs)
