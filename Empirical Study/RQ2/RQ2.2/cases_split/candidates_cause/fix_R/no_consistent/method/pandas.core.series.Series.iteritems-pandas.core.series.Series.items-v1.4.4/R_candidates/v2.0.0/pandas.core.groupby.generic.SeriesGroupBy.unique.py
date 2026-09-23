    @doc(Series.unique.__doc__)
    def unique(self) -> Series:
        result = self._op_via_apply("unique")
        return result
