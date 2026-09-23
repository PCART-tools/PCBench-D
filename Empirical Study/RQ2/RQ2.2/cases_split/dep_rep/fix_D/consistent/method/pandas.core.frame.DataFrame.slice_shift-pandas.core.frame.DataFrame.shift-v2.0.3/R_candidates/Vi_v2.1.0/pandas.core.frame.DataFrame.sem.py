    @doc(make_doc("sem", ndim=2))
    def sem(
        self,
        axis: Axis | None = 0,
        skipna: bool = True,
        ddof: int = 1,
        numeric_only: bool = False,
        **kwargs,
    ):
        result = super().sem(axis, skipna, ddof, numeric_only, **kwargs)
        if isinstance(result, Series):
            result = result.__finalize__(self, method="sem")
        return result
