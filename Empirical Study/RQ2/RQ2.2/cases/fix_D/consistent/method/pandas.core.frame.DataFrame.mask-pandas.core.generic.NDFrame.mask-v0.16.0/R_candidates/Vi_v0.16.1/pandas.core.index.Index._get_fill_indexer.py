    def _get_fill_indexer(self, target, method, limit=None):
        if self.is_monotonic_increasing and target.is_monotonic_increasing:
            method = (self._engine.get_pad_indexer if method == 'pad'
                      else self._engine.get_backfill_indexer)
            indexer = method(target.values, limit)
        else:
            indexer = self._get_fill_indexer_searchsorted(target, method, limit)
        return indexer
