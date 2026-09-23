class CaseInsensitiveMultiDict(MultiDict):
    """Case insensitive multi dict."""

    def getall(self, key):
        return tuple(self._items[key.upper()])

    def get(self, key, default=None):
        key = key.upper()
        if key in self._items and self._items[key]:
            return self._items[key][0]
        else:
            return default

    def getone(self, key):
        return self._items[key.upper()][0]

    def __getitem__(self, key):
        return self._items[key.upper()][0]

    def __contains__(self, key):
        return key.upper() in self._items
