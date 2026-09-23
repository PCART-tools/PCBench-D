    def _reindex_index(
        self,
        new_index,
        method,
        copy: bool,
        level: Level,
        fill_value=np.nan,
        limit=None,
        tolerance=None,
    ):
        new_index, indexer = self.index.reindex(
            new_index, method=method, level=level, limit=limit, tolerance=tolerance
        )
        return self._reindex_with_indexers(
            {0: [new_index, indexer]},
            copy=copy,
            fill_value=fill_value,
            allow_dups=False,
        )
