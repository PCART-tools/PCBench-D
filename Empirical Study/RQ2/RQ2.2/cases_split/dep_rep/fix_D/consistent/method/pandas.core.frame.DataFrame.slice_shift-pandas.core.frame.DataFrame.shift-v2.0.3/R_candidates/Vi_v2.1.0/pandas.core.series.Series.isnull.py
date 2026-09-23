    @doc(NDFrame.isna, klass=_shared_doc_kwargs["klass"])  # type: ignore[has-type]
    def isnull(self) -> Series:
        """
        Series.isnull is an alias for Series.isna.
        """
        return super().isnull()
