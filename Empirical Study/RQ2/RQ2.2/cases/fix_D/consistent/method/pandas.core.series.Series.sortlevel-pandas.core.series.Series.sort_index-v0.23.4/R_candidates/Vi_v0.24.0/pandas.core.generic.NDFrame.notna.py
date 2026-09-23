    @Appender(_shared_docs['notna'] % _shared_doc_kwargs)
    def notna(self):
        return notna(self).__finalize__(self)
