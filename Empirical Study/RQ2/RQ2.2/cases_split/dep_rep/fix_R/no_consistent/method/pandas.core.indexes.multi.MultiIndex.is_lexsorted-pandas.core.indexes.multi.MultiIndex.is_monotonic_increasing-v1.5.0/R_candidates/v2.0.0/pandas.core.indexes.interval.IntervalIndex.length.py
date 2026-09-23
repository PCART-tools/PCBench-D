    @property
    def length(self) -> Index:
        return Index(self._data.length, copy=False)
