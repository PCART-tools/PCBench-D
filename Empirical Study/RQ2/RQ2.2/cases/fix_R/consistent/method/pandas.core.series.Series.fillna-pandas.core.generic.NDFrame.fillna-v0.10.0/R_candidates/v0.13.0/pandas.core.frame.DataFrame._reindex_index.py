    def _reindex_index(self, new_index, method, copy, level, fill_value=NA,
                       limit=None, takeable=False):
        new_index, indexer = self.index.reindex(new_index, method, level,
                                                limit=limit,
                                                copy_if_needed=True,
                                                takeable=takeable)
        return self._reindex_with_indexers({0: [new_index, indexer]},
                                           copy=copy, fill_value=fill_value,
                                           allow_dups=takeable)
