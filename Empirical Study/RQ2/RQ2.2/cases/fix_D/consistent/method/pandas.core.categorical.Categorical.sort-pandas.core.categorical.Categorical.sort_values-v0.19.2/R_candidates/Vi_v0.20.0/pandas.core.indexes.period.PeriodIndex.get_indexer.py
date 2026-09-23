    @Appender(_index_shared_docs['get_indexer'] % _index_doc_kwargs)
    def get_indexer(self, target, method=None, limit=None, tolerance=None):
        target = _ensure_index(target)

        if hasattr(target, 'freq') and target.freq != self.freq:
            msg = _DIFFERENT_FREQ_INDEX.format(self.freqstr, target.freqstr)
            raise IncompatibleFrequency(msg)

        if isinstance(target, PeriodIndex):
            target = target.asi8

        if tolerance is not None:
            tolerance = self._convert_tolerance(tolerance)
        return Index.get_indexer(self._int64index, target, method,
                                 limit, tolerance)
