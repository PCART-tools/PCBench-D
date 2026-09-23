    @Appender(_shared_docs["notna"] % _shared_doc_kwargs)
    def notna(self) -> "DataFrame":
        return super().notna()
