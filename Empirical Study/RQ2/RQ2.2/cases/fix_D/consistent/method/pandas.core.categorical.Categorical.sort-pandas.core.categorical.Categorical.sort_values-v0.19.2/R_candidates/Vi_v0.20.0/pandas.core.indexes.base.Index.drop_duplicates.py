    @Appender(base._shared_docs['drop_duplicates'] % _index_doc_kwargs)
    def drop_duplicates(self, keep='first'):
        return super(Index, self).drop_duplicates(keep=keep)
