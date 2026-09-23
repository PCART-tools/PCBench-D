    def _getitem_array(self, key):
        # also raises Exception if object array with NA values
        if com.is_bool_indexer(key):
            # warning here just in case -- previously __setitem__ was
            # reindexing but __getitem__ was not; it seems more reasonable to
            # go with the __setitem__ behavior since that is more consistent
            # with all other indexing behavior
            if isinstance(key, Series) and not key.index.equals(self.index):
                warnings.warn("Boolean Series key will be reindexed to match "
                              "DataFrame index.", UserWarning, stacklevel=3)
            elif len(key) != len(self.index):
                raise ValueError('Item wrong length %d instead of %d.' %
                                 (len(key), len(self.index)))
            # check_bool_indexer will throw exception if Series key cannot
            # be reindexed to match DataFrame rows
            key = check_bool_indexer(self.index, key)
            indexer = key.nonzero()[0]
            return self._take(indexer, axis=0)
        else:
            indexer = self.loc._convert_to_indexer(key, axis=1)
            return self._take(indexer, axis=1)
