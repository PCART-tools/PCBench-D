    @doc(make_doc("skew", ndim=1))
    def skew(
        self,
        axis: Axis | None = 0,
        skipna: bool = True,
        numeric_only: bool = False,
        **kwargs,
    ):
        return NDFrame.skew(self, axis, skipna, numeric_only, **kwargs)
