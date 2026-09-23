    def __getitem__(self, tag: int) -> Any:
        if self._info is not None and tag not in self._data and tag in self._info:
            self._data[tag] = self._fixup(self._info[tag])
            del self._info[tag]
        return self._data[tag]
