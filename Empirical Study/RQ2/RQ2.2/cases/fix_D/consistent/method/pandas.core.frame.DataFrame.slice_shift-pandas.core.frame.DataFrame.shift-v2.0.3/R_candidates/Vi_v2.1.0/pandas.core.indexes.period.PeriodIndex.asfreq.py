    @doc(
        PeriodArray.asfreq,
        other="pandas.arrays.PeriodArray",
        other_name="PeriodArray",
        **_shared_doc_kwargs,
    )
    def asfreq(self, freq=None, how: str = "E") -> Self:
        arr = self._data.asfreq(freq, how)
        return type(self)._simple_new(arr, name=self.name)
