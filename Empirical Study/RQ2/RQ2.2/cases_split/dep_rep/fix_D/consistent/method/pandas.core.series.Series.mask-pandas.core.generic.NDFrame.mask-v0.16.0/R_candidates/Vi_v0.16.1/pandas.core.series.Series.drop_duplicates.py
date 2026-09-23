    @Appender(base._shared_docs['drop_duplicates'] % _shared_doc_kwargs)
    def drop_duplicates(self, take_last=False, inplace=False):
        return super(Series, self).drop_duplicates(take_last=take_last,
                                                   inplace=inplace)
