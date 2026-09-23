    @doc(make_doc("std", ndim=1))
    def std(
        self,
        axis: Axis | None = None,
        skipna: bool = True,
        ddof: int = 1,
        numeric_only: bool = False,
        **kwargs,
    ):
        return NDFrame.std(self, axis, skipna, ddof, numeric_only, **kwargs)
