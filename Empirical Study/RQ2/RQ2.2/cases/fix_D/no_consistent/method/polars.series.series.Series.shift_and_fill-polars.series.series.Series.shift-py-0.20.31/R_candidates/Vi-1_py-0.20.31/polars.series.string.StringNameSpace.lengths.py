    @deprecate_renamed_function("len_bytes", version="0.19.8")
    def lengths(self) -> Series:
        """
        Return the number of bytes in each string.

        .. deprecated:: 0.19.8
            This method has been renamed to :func:`len_bytes`.
        """
