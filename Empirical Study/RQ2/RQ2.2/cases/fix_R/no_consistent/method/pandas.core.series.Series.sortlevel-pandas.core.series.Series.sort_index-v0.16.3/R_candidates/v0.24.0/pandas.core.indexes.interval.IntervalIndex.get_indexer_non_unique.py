    @Appender(_index_shared_docs['get_indexer_non_unique'] % _index_doc_kwargs)
    def get_indexer_non_unique(self, target):
        target = self._maybe_cast_indexed(ensure_index(target))
        return super(IntervalIndex, self).get_indexer_non_unique(target)
