    @doc(isna, klass=_shared_doc_kwargs["klass"])
    def isnull(self: NDFrameT) -> NDFrameT:
        return isna(self).__finalize__(self, method="isnull")
