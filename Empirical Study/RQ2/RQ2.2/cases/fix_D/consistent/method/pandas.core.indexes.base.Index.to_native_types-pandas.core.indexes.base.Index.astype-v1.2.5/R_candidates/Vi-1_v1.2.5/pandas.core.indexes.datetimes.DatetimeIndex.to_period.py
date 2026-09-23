    @doc(DatetimeArray.to_period)
    def to_period(self, freq=None) -> "PeriodIndex":
        from pandas.core.indexes.api import PeriodIndex

        arr = self._data.to_period(freq)
        return PeriodIndex._simple_new(arr, name=self.name)
