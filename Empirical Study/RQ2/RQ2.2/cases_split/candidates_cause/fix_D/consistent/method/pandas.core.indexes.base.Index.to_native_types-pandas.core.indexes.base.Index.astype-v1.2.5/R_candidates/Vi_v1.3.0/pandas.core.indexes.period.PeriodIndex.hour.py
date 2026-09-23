    @property  # type:ignore[misc]
    @doc(PeriodArray.hour.fget)
    def hour(self) -> Int64Index:
        return Int64Index(self._data.hour, name=self.name)
