    def __delitem__(self, tag: int) -> None:
        if self._info is not None and tag in self._info:
            del self._info[tag]
        else:
            del self._data[tag]
