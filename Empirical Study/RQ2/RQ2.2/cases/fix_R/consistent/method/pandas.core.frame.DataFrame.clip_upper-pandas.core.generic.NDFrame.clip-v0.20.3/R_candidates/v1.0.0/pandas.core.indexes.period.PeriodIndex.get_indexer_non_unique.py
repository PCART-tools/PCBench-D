    @Appender(_index_shared_docs["get_indexer_non_unique"] % _index_doc_kwargs)
    def get_indexer_non_unique(self, target):
        target = ensure_index(target)

        if isinstance(target, PeriodIndex):
            if target.freq != self.freq:
                no_matches = -1 * np.ones(self.shape, dtype=np.intp)
                return no_matches, no_matches

            target = target.asi8

        indexer, missing = self._int64index.get_indexer_non_unique(target)
        return ensure_platform_int(indexer), missing
