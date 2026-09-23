    def __setitem__(self, key, value):
        # kludgetastic
        ax = self.obj._get_axis(0)
        if isinstance(ax, MultiIndex):
            try:
                indexer = ax.get_loc(key)
                self._setitem_with_indexer(indexer, value)
                return
            except Exception:
                pass

        if isinstance(key, tuple):
            if len(key) > self.ndim:
                raise IndexingError('only tuples of length <= %d supported' %
                                    self.ndim)
            indexer = self._convert_tuple(key, is_setter=True)
        else:
            indexer = self._convert_to_indexer(key, is_setter=True)

        self._setitem_with_indexer(indexer, value)
