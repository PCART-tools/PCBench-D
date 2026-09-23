    def __setitem__(self, key, value):
        if isinstance(key, tuple):
            key = tuple(com.apply_if_callable(x, self.obj)
                        for x in key)
        else:
            key = com.apply_if_callable(key, self.obj)
        indexer = self._get_setitem_indexer(key)
        self._setitem_with_indexer(indexer, value)
