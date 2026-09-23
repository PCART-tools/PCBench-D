    @Appender(_index_shared_docs['contains'] % _index_doc_kwargs)
    def contains(self, key):
        hash(key)
        try:
            return key in self._engine
        except (TypeError, ValueError):
            return False
