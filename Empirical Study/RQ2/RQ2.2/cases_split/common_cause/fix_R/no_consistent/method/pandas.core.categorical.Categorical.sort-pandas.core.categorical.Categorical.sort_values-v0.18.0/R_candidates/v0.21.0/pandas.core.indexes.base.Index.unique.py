    @Appender(base._shared_docs['unique'] % _index_doc_kwargs)
    def unique(self):
        result = super(Index, self).unique()
        return self._shallow_copy(result)
