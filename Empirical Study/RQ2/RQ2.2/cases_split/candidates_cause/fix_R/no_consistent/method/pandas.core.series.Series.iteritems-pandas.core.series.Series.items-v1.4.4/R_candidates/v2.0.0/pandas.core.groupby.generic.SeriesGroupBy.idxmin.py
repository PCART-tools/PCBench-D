    @doc(Series.idxmin.__doc__)
    def idxmin(self, axis: Axis = 0, skipna: bool = True) -> Series:
        result = self._op_via_apply("idxmin", axis=axis, skipna=skipna)
        return result
