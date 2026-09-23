    @doc(PeriodArray.to_timestamp)
    def to_timestamp(self, freq=None, how: str = "start") -> DatetimeIndex:
        arr = self._data.to_timestamp(freq, how)
        return DatetimeIndex._simple_new(arr, name=self.name)
