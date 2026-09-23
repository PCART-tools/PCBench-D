    @Appender(generic._shared_docs['isna'] % _shared_doc_kwargs)
    def isnull(self):
        return super(Series, self).isnull()
