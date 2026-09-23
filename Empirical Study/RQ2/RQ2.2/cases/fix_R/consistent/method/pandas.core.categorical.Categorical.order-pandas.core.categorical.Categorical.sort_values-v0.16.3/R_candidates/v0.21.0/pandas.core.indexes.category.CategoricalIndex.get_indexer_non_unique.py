    @Appender(_index_shared_docs['get_indexer_non_unique'] % _index_doc_kwargs)
    def get_indexer_non_unique(self, target):
        target = ibase._ensure_index(target)

        if isinstance(target, CategoricalIndex):
            target = target.categories

        codes = self.categories.get_indexer(target)
        indexer, missing = self._engine.get_indexer_non_unique(codes)
        return _ensure_platform_int(indexer), missing
