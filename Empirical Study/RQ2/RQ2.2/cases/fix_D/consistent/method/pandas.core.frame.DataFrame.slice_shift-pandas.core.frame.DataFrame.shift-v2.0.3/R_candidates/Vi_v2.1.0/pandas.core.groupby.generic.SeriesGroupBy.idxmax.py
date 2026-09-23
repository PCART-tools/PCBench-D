    @doc(Series.idxmax.__doc__)
    def idxmax(
        self, axis: Axis | lib.NoDefault = lib.no_default, skipna: bool = True
    ) -> Series:
        result = self._op_via_apply("idxmax", axis=axis, skipna=skipna)
        return result.astype(self.obj.index.dtype) if result.empty else result
