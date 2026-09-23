    @doc(Series.idxmax.__doc__)
    def idxmax(self, axis: Axis = 0, skipna: bool = True) -> Series:
        result = self._op_via_apply("idxmax", axis=axis, skipna=skipna)
        return result
