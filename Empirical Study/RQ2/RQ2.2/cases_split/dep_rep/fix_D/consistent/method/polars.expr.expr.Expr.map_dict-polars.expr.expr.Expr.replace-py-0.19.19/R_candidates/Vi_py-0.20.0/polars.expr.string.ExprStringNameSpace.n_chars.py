    @deprecate_renamed_function("len_chars", version="0.19.8")
    def n_chars(self) -> Expr:
        """
        Return the length of each string as the number of characters.

        .. deprecated:: 0.19.8
            This method has been renamed to :func:`len_chars`.

        """
        return self.len_chars()
