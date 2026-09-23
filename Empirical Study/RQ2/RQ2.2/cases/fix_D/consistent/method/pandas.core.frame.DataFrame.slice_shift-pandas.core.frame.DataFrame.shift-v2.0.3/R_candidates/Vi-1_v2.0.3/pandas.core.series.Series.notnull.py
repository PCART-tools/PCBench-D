    @doc(NDFrame.notna, klass=_shared_doc_kwargs["klass"])  # type: ignore[has-type]
    def notnull(self) -> Series:
        """
        Series.notnull is an alias for Series.notna.
        """
        return super().notnull()
