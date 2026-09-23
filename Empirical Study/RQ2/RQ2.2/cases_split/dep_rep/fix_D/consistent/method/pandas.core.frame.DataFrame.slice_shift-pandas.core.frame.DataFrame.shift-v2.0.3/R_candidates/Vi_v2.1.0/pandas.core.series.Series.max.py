    @doc(make_doc("max", ndim=1))
    def max(
        self,
        axis: Axis | None = 0,
        skipna: bool = True,
        numeric_only: bool = False,
        **kwargs,
    ):
        return NDFrame.max(self, axis, skipna, numeric_only, **kwargs)
