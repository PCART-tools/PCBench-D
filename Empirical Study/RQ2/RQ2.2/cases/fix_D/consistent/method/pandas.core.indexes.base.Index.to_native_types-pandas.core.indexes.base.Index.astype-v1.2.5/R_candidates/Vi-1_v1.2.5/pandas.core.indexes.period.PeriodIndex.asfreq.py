    @doc(PeriodArray.asfreq)
    def asfreq(self, freq=None, how: str = "E") -> "PeriodIndex":
        arr = self._data.asfreq(freq, how)
        return type(self)._simple_new(arr, name=self.name)
