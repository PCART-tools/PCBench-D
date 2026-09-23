    @doc(notna, klass=_shared_doc_kwargs["klass"])
    def notnull(self: NDFrameT) -> NDFrameT:
        return notna(self).__finalize__(self, method="notnull")
