    @cache_readonly
    @Appender(_interval_shared_docs['is_non_overlapping_monotonic']
              % _index_doc_kwargs)
    def is_non_overlapping_monotonic(self):
        return self._data.is_non_overlapping_monotonic
