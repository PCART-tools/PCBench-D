    @Appender(_index_shared_docs["get_indexer"] % _index_doc_kwargs)
    def get_indexer(self, target, method=None, limit=None, tolerance=None):
        target = ensure_index(target)

        if isinstance(target, PeriodIndex):
            if target.freq != self.freq:
                # No matches
                no_matches = -1 * np.ones(self.shape, dtype=np.intp)
                return no_matches

            target = target.asi8
            self_index = self._int64index
        else:
            self_index = self

        if tolerance is not None:
            tolerance = self._convert_tolerance(tolerance, target)
        return Index.get_indexer(self_index, target, method, limit, tolerance)
