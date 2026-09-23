    @Appender(_shared_docs['duplicated'] % _index_doc_kwargs)
    def duplicated(self, take_last=False):
        return super(Index, self).duplicated(take_last=take_last)
