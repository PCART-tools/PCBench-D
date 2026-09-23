    def _reindex_columns(self, new_columns, copy, level, fill_value=NA,
                         limit=None, takeable=False):
        new_columns, indexer = self.columns.reindex(new_columns, level=level,
                                                    limit=limit,
                                                    copy_if_needed=True,
                                                    takeable=takeable)
        return self._reindex_with_indexers({1: [new_columns, indexer]},
                                           copy=copy, fill_value=fill_value,
                                           allow_dups=takeable)
