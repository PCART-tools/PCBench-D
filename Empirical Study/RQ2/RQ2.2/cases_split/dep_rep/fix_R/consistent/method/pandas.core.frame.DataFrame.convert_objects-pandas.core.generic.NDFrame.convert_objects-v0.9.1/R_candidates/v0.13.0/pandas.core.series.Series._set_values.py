    def _set_values(self, key, value):
        if isinstance(key, Series):
            key = key.values
        self._data = self._data.setitem(key, value)
