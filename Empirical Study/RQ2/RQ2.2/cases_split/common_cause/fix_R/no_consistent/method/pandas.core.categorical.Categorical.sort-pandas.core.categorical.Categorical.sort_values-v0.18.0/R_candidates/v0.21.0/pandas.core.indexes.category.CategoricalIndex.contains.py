    @Appender(_index_shared_docs['contains'] % _index_doc_kwargs)
    def contains(self, key):
        hash(key)

        if self.categories._defer_to_indexing:
            return self.categories.contains(key)

        return key in self.values
