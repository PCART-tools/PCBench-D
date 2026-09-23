    @Appender(_shared_docs["notna"] % _shared_doc_kwargs)
    def notnull(self) -> "DataFrame":
        return super().notnull()
