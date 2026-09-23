    @Appender(_index_shared_docs['contains'] % _index_doc_kwargs)
    def contains(self, key):
        return key in self
