    @Appender(_index_shared_docs['__contains__'] % _index_doc_kwargs)
    def __contains__(self, key):
        hash(key)
        try:
            return key in self._engine
        except (OverflowError, TypeError, ValueError):
            return False
