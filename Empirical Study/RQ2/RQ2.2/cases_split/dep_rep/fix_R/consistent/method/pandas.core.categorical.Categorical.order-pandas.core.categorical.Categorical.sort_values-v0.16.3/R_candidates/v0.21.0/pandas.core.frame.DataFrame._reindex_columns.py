    def _reindex_columns(self, new_columns, method, copy, level,
                         fill_value=np.nan, limit=None, tolerance=None):
        new_columns, indexer = self.columns.reindex(new_columns, method=method,
                                                    level=level, limit=limit,
                                                    tolerance=tolerance)
        return self._reindex_with_indexers({1: [new_columns, indexer]},
                                           copy=copy, fill_value=fill_value,
                                           allow_dups=False)
