    @doc(DatetimeArray.to_perioddelta)
    def to_perioddelta(self, freq) -> TimedeltaIndex:
        from pandas.core.indexes.api import TimedeltaIndex

        arr = self._data.to_perioddelta(freq)
        return TimedeltaIndex._simple_new(arr, name=self.name)
