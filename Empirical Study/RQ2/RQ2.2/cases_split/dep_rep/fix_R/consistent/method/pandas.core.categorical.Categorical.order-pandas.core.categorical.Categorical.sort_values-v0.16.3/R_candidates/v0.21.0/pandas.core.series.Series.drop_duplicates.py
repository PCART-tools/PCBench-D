    @Appender(base._shared_docs['drop_duplicates'] % _shared_doc_kwargs)
    def drop_duplicates(self, keep='first', inplace=False):
        return super(Series, self).drop_duplicates(keep=keep, inplace=inplace)
