    @Appender(_shared_docs['isna'] % _shared_doc_kwargs)
    def isna(self):
        return isna(self).__finalize__(self)
