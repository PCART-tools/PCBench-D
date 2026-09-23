    def _getitem_tuple(self, tup: tuple):
        with suppress(IndexingError):
            tup = self._expand_ellipsis(tup)
            return self._getitem_lowerdim(tup)

        # no multi-index, so validate all of the indexers
        tup = self._validate_tuple_indexer(tup)

        # ugly hack for GH #836
        if self._multi_take_opportunity(tup):
            return self._multi_take(tup)

        return self._getitem_tuple_same_dim(tup)
