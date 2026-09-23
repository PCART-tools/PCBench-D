    @doc(make_doc("var", ndim=1))
    def var(
        self,
        axis: Axis | None = None,
        skipna: bool = True,
        ddof: int = 1,
        numeric_only: bool = False,
        **kwargs,
    ):
        return NDFrame.var(self, axis, skipna, ddof, numeric_only, **kwargs)
