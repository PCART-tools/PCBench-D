    def _setitem_with_indexer(self, indexer, value):

        # need to delegate to the super setter
        if isinstance(indexer, dict):
            return super(_SeriesIndexer, self)._setitem_with_indexer(indexer,
                                                                     value)

        # fast access
        self.obj._set_values(indexer, value)
