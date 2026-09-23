    @deprecate_renamed_function("len_bytes", version="0.19.8")
    def lengths(self) -> Expr:
        """
        Return the length of each string as the number of bytes.

        .. deprecated:: 0.19.8
            This method has been renamed to :func:`len_bytes`.
        """
        return self.len_bytes()
