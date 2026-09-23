    def _set_item(self, key, value):
        self._data.set(key, value)
        self._clear_item_cache()
