    @doc(NDFrame.isna, klass=_shared_doc_kwargs["klass"])
    def isnull(self) -> DataFrame:
        """
        DataFrame.isnull is an alias for DataFrame.isna.
        """
        return self.isna()
