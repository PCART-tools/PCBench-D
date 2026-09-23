    @doc(make_doc("any", ndim=2))
    # error: Signature of "any" incompatible with supertype "NDFrame"
    def any(  # type: ignore[override]
        self,
        *,
        axis: Axis = 0,
        bool_only: bool = False,
        skipna: bool = True,
        **kwargs,
    ) -> Series | bool:
        result = self._logical_func(
            "any", nanops.nanany, axis, bool_only, skipna, **kwargs
        )
        if isinstance(result, Series):
            result = result.__finalize__(self, method="any")
        return result
