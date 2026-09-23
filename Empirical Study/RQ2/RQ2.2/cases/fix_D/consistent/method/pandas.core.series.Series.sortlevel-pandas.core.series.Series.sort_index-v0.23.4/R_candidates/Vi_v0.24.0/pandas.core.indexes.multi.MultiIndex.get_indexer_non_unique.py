    @Appender(_index_shared_docs['get_indexer_non_unique'] % _index_doc_kwargs)
    def get_indexer_non_unique(self, target):
        return super(MultiIndex, self).get_indexer_non_unique(target)
