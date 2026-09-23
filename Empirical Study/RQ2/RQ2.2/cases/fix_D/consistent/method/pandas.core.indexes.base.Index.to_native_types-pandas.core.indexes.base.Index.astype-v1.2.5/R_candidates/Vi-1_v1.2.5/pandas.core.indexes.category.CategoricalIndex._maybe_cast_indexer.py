    def _maybe_cast_indexer(self, key) -> int:
        return self._data._unbox_scalar(key)
