    @Appender(generic._shared_docs['notna'] % _shared_doc_kwargs)
    def notnull(self):
        return super(Series, self).notnull()
