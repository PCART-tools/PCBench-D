    @property  # type: ignore[misc]
    @doc(PeriodArray.minute.fget)
    def minute(self) -> Int64Index:
        return Int64Index(self._data.minute, name=self.name)
