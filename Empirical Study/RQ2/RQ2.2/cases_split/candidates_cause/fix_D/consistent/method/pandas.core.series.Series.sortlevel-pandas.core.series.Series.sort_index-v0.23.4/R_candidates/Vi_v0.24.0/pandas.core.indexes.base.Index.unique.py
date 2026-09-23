    @Appender(_index_shared_docs['index_unique'] % _index_doc_kwargs)
    def unique(self, level=None):
        if level is not None:
            self._validate_index_level(level)
        result = super(Index, self).unique()
        return self._shallow_copy(result)
