    @doc(make_doc("all", ndim=2))
    def all(
        self,
        axis: Axis = 0,
        bool_only: bool = False,
        skipna: bool = True,
        **kwargs,
    ) -> Series | bool:
        result = self._logical_func(
            "all", nanops.nanall, axis, bool_only, skipna, **kwargs
        )
        if isinstance(result, Series):
            result = result.__finalize__(self, method="all")
        return result
