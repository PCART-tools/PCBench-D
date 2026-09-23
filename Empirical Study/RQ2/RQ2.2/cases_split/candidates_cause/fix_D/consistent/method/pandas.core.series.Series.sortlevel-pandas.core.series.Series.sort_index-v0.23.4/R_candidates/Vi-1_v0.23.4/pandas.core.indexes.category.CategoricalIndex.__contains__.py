    @Appender(_index_shared_docs['__contains__'] % _index_doc_kwargs)
    def __contains__(self, key):
        hash(key)

        if self.categories._defer_to_indexing:
            return key in self.categories

        return key in self.values
