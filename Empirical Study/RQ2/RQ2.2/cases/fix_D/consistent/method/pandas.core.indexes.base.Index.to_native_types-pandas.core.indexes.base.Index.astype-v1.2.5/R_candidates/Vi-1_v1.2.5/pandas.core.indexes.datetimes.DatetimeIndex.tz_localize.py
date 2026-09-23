    @doc(DatetimeArray.tz_localize)
    def tz_localize(
        self, tz, ambiguous="raise", nonexistent="raise"
    ) -> "DatetimeIndex":
        arr = self._data.tz_localize(tz, ambiguous, nonexistent)
        return type(self)._simple_new(arr, name=self.name)
