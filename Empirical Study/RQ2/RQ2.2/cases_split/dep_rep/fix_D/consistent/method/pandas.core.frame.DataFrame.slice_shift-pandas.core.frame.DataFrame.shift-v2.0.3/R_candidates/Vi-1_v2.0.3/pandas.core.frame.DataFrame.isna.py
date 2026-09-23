    @doc(NDFrame.isna, klass=_shared_doc_kwargs["klass"])
    def isna(self) -> DataFrame:
        result = self._constructor(self._mgr.isna(func=isna))
        return result.__finalize__(self, method="isna")
