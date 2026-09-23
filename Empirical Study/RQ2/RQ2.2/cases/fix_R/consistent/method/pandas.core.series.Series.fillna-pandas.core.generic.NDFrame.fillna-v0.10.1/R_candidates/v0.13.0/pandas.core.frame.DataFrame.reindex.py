    @Appender(_shared_docs['reindex'] % _shared_doc_kwargs)
    def reindex(self, index=None, columns=None, **kwargs):
        return super(DataFrame, self).reindex(index=index, columns=columns,
                                              **kwargs)
