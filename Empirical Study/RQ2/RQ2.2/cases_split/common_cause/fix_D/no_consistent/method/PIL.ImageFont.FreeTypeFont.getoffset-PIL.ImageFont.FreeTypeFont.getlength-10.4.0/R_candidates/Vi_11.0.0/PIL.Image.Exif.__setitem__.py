    def __setitem__(self, tag: int, value: Any) -> None:
        if self._info is not None and tag in self._info:
            del self._info[tag]
        self._data[tag] = value
