    @doc(Series.idxmin.__doc__)
    def idxmin(
        self, axis: Axis | lib.NoDefault = lib.no_default, skipna: bool = True
    ) -> Series:
        result = self._op_via_apply("idxmin", axis=axis, skipna=skipna)
        return result.astype(self.obj.index.dtype) if result.empty else result
