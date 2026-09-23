    def _set_axis(self, axis, labels) -> None:
        self._data.set_axis(axis, labels)
        self._clear_item_cache()
