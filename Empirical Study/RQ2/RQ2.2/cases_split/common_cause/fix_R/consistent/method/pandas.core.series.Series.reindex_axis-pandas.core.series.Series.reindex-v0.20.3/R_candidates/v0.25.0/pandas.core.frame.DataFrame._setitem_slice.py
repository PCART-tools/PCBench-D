    def _setitem_slice(self, key, value):
        self._check_setitem_copy()
        self.loc._setitem_with_indexer(key, value)
