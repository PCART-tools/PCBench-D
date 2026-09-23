    @doc(DatetimeArray.isocalendar)
    def isocalendar(self) -> "DataFrame":
        df = self._data.isocalendar()
        return df.set_index(self)
