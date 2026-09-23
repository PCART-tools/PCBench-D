    def median(
        self,
        *,
        axis: int | None = None,
        out=None,
        overwrite_input: bool = False,
        keepdims: bool = False,
        skipna: bool = True,
    ):
        nv.validate_median(
            (), {"out": out, "overwrite_input": overwrite_input, "keepdims": keepdims}
        )
        result = nanops.nanmedian(self._ndarray, axis=axis, skipna=skipna)
        return self._wrap_reduction_result(axis, result)
