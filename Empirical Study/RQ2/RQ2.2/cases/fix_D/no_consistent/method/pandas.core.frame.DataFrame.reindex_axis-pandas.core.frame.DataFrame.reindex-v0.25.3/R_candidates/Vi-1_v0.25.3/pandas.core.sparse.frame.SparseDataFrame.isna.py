    @Appender(generic._shared_docs["isna"] % _shared_doc_kwargs)
    def isna(self):
        return self._apply_columns(lambda x: x.isna())
