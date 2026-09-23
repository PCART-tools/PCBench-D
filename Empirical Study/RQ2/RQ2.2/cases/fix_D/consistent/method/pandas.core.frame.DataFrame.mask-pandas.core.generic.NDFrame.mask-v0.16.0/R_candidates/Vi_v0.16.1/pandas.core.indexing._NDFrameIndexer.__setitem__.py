    def __setitem__(self, key, value):
        indexer = self._get_setitem_indexer(key)
        self._setitem_with_indexer(indexer, value)
