    @doc(NDFrame.notna, klass=_shared_doc_kwargs["klass"])
    def notnull(self) -> DataFrame:
        """
        DataFrame.notnull is an alias for DataFrame.notna.
        """
        return ~self.isna()
