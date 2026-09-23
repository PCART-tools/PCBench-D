    @Appender(_index_shared_docs["get_indexer"] % _index_doc_kwargs)
    def get_indexer(self, target, method=None, limit=None, tolerance=None):
        method = missing.clean_reindex_fill_method(method)
        target = ibase.ensure_index(target)

        self._check_indexing_method(method)

        if self.is_unique and self.equals(target):
            return np.arange(len(self), dtype="intp")

        return self._get_indexer_non_unique(target._values)[0]
