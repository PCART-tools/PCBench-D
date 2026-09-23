    @doc(notna, klass=_shared_doc_kwargs["klass"])
    def notnull(self) -> Self:
        return notna(self).__finalize__(self, method="notnull")
