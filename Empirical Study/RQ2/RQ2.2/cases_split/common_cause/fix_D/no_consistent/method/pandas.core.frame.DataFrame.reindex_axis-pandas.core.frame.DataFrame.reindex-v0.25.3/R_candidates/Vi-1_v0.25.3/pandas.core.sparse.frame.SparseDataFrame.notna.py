    @Appender(generic._shared_docs["notna"] % _shared_doc_kwargs)
    def notna(self):
        return self._apply_columns(lambda x: x.notna())
