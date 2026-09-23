    @Appender(_shared_docs["notna"] % _shared_doc_kwargs)
    def notnull(self):
        return notna(self).__finalize__(self)
