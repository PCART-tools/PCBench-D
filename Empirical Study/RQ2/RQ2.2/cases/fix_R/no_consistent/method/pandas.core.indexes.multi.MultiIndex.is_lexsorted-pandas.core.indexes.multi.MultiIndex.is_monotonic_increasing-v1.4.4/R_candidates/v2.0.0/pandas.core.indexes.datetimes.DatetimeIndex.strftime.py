    @doc(DatetimeArray.strftime)
    def strftime(self, date_format) -> Index:
        arr = self._data.strftime(date_format)
        return Index(arr, name=self.name, dtype=object)
