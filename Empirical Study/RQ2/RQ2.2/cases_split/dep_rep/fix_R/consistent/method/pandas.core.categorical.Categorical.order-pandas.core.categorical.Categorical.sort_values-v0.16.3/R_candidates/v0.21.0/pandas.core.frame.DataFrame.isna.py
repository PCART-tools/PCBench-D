    @Appender(_shared_docs['isna'] % _shared_doc_kwargs)
    def isna(self):
        return super(DataFrame, self).isna()
