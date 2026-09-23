    @doc(NDFrame.notna, klass=_shared_doc_kwargs["klass"])
    def notna(self) -> DataFrame:
        return ~self.isna()
