    @doc(NDFrame.isna, klass=_shared_doc_kwargs["klass"])  # type: ignore[has-type]
    def isna(self) -> Series:  # type: ignore[override]
        return NDFrame.isna(self)
