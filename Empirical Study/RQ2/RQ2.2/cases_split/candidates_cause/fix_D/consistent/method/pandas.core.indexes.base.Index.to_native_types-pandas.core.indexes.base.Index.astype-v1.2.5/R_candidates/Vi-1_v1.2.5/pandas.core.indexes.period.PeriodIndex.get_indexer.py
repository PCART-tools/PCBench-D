    @Appender(_index_shared_docs["get_indexer"] % _index_doc_kwargs)
    def get_indexer(self, target, method=None, limit=None, tolerance=None):
        target = ensure_index(target)

        if not self._should_compare(target):
            return self._get_indexer_non_comparable(target, method, unique=True)

        if isinstance(target, PeriodIndex):
            target = target._get_engine_target()  # i.e. target.asi8
            self_index = self._int64index
        else:
            self_index = self

        if tolerance is not None:
            tolerance = self._convert_tolerance(tolerance, target)
            if self_index is not self:
                # convert tolerance to i8
                tolerance = self._maybe_convert_timedelta(tolerance)

        return Index.get_indexer(self_index, target, method, limit, tolerance)
