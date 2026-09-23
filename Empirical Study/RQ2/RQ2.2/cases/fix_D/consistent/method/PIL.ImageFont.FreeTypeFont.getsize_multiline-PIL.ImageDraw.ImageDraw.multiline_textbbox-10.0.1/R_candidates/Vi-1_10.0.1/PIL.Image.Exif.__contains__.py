    def __contains__(self, tag):
        return tag in self._data or (self._info is not None and tag in self._info)
