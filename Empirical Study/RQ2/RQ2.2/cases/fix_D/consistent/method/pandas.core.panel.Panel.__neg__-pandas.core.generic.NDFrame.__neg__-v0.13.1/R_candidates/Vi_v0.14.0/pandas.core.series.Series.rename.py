    @Appender(generic._shared_docs['rename'] % _shared_doc_kwargs)
    def rename(self, index=None, **kwargs):
        return super(Series, self).rename(index=index, **kwargs)
