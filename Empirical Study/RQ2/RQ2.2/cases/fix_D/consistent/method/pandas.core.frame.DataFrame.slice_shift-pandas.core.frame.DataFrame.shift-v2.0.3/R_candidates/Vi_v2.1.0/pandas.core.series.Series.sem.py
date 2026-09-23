    @doc(make_doc("sem", ndim=1))
    def sem(
        self,
        axis: Axis | None = None,
        skipna: bool = True,
        ddof: int = 1,
        numeric_only: bool = False,
        **kwargs,
    ):
        return NDFrame.sem(self, axis, skipna, ddof, numeric_only, **kwargs)
