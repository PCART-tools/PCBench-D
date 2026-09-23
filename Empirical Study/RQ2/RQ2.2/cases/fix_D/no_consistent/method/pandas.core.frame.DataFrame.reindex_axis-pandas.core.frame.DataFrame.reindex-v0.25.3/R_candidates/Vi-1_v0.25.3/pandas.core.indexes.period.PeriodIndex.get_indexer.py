    @Appender(_index_shared_docs["get_indexer"] % _index_doc_kwargs)
    def get_indexer(self, target, method=None, limit=None, tolerance=None):
        target = ensure_index(target)

        if hasattr(target, "freq") and target.freq != self.freq:
            msg = DIFFERENT_FREQ.format(
                cls=type(self).__name__,
                own_freq=self.freqstr,
                other_freq=target.freqstr,
            )
            raise IncompatibleFrequency(msg)

        if isinstance(target, PeriodIndex):
            target = target.asi8

        if tolerance is not None:
            tolerance = self._convert_tolerance(tolerance, target)
        return Index.get_indexer(self._int64index, target, method, limit, tolerance)
