    @doc(make_doc("mean", ndim=1))
    def mean(
        self,
        axis: Axis | None = 0,
        skipna: bool = True,
        numeric_only: bool = False,
        **kwargs,
    ):
        return NDFrame.mean(self, axis, skipna, numeric_only, **kwargs)
