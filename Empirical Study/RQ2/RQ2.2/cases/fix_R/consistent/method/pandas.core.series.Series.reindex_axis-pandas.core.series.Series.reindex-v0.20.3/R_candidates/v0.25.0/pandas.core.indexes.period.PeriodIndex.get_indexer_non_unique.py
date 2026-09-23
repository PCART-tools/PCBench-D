    @Appender(_index_shared_docs["get_indexer_non_unique"] % _index_doc_kwargs)
    def get_indexer_non_unique(self, target):
        target = ensure_index(target)

        if isinstance(target, PeriodIndex):
            target = target.asi8
            if hasattr(target, "freq") and target.freq != self.freq:
                msg = DIFFERENT_FREQ.format(
                    cls=type(self).__name__,
                    own_freq=self.freqstr,
                    other_freq=target.freqstr,
                )
                raise IncompatibleFrequency(msg)

        indexer, missing = self._int64index.get_indexer_non_unique(target)
        return ensure_platform_int(indexer), missing
