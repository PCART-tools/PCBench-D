    @doc(make_doc("median", ndim=1))
    def median(
        self,
        axis: Axis | None = 0,
        skipna: bool = True,
        numeric_only: bool = False,
        **kwargs,
    ):
        return NDFrame.median(self, axis, skipna, numeric_only, **kwargs)
