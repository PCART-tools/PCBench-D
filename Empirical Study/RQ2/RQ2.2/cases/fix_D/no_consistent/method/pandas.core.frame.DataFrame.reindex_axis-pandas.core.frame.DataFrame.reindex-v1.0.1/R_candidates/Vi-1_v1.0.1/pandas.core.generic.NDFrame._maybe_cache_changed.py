    def _maybe_cache_changed(self, item, value) -> None:
        """The object has called back to us saying maybe it has changed.
        """
        self._data.set(item, value)
