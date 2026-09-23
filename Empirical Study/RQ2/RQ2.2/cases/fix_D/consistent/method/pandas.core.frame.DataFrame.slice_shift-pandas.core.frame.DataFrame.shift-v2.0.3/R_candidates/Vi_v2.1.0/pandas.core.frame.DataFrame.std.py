    @doc(make_doc("std", ndim=2))
    def std(
        self,
        axis: Axis | None = 0,
        skipna: bool = True,
        ddof: int = 1,
        numeric_only: bool = False,
        **kwargs,
    ):
        result = super().std(axis, skipna, ddof, numeric_only, **kwargs)
        if isinstance(result, Series):
            result = result.__finalize__(self, method="std")
        return result
