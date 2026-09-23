    def _set_values(self, key, value):
        if isinstance(key, Series):
            key = key._values
        self._data = self._data.setitem(indexer=key, value=value)
        self._maybe_update_cacher()
