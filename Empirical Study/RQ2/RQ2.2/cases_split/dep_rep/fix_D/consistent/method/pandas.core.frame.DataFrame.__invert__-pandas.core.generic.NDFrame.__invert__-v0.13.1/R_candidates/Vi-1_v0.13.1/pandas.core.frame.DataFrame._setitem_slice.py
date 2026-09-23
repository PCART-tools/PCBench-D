    def _setitem_slice(self, key, value):
        self._check_setitem_copy()
        self.ix._setitem_with_indexer(key, value)
