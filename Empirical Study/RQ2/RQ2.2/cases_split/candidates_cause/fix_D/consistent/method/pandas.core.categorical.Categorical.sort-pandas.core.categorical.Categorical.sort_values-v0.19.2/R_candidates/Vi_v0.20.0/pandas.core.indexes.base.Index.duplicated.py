    @Appender(base._shared_docs['duplicated'] % _index_doc_kwargs)
    def duplicated(self, keep='first'):
        return super(Index, self).duplicated(keep=keep)
