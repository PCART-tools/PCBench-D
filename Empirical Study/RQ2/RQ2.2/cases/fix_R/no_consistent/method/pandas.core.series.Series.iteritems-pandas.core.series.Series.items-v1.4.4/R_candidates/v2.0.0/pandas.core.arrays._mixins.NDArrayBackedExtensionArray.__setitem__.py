    def __setitem__(self, key, value) -> None:
        key = check_array_indexer(self, key)
        value = self._validate_setitem_value(value)
        self._ndarray[key] = value
