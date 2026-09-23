    @Appender(_shared_docs['drop_duplicates'] % _index_doc_kwargs)
    def drop_duplicates(self, take_last=False):
        result = super(Index, self).drop_duplicates(take_last=take_last)
        return self._constructor(result)
