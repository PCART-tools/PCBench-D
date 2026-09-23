    @Appender(_index_shared_docs['contains'] % _index_doc_kwargs)
    def __contains__(self, key):
        # if key is a NaN, check if any NaN is in self.
        if isna(key):
            return self.hasnans

        return contains(self, key, container=self._engine)
