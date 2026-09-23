    @Appender(_shared_docs['rename'] % _shared_doc_kwargs)
    def rename(self, index=None, columns=None, **kwargs):
        return super(DataFrame, self).rename(index=index, columns=columns,
                                             **kwargs)
