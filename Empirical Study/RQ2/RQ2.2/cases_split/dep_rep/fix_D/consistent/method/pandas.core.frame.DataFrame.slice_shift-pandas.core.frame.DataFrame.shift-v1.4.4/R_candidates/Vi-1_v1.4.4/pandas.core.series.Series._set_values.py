    def _set_values(self, key, value) -> None:
        if isinstance(key, (Index, Series)):
            key = key._values

        self._mgr = self._mgr.setitem(indexer=key, value=value)
        self._maybe_update_cacher()
