    @doc(NDFrame.isna, klass=_shared_doc_kwargs["klass"])
    def isna(self) -> DataFrame:
        res_mgr = self._mgr.isna(func=isna)
        result = self._constructor_from_mgr(res_mgr, axes=res_mgr.axes)
        return result.__finalize__(self, method="isna")
