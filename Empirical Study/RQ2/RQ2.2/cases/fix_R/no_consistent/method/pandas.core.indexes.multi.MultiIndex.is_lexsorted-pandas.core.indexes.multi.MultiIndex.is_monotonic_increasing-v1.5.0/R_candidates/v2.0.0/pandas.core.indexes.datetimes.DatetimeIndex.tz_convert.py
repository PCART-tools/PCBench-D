    @doc(DatetimeArray.tz_convert)
    def tz_convert(self, tz) -> DatetimeIndex:
        arr = self._data.tz_convert(tz)
        return type(self)._simple_new(arr, name=self.name, refs=self._references)
