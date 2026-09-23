    @Appender(_index_shared_docs['get_indexer'] % _index_doc_kwargs)
    def get_indexer(self, target, method=None, limit=None, tolerance=None):

        self._check_method(method)
        target = ensure_index(target)
        target = self._maybe_cast_indexed(target)

        if self.equals(target):
            return np.arange(len(self), dtype='intp')

        if self.is_non_overlapping_monotonic:
            start, stop = self._find_non_overlapping_monotonic_bounds(target)

            start_plus_one = start + 1
            if not ((start_plus_one < stop).any()):
                return np.where(start_plus_one == stop, start, -1)

        if not self.is_unique:
            raise ValueError("cannot handle non-unique indices")

        # IntervalIndex
        if isinstance(target, IntervalIndex):
            indexer = self._get_reindexer(target)

        # non IntervalIndex
        else:
            indexer = np.concatenate([self.get_loc(i) for i in target])

        return ensure_platform_int(indexer)
