    @property  # type:ignore[misc]
    @doc(PeriodArray.second.fget)
    def second(self) -> Int64Index:
        return Int64Index(self._data.second, name=self.name)
