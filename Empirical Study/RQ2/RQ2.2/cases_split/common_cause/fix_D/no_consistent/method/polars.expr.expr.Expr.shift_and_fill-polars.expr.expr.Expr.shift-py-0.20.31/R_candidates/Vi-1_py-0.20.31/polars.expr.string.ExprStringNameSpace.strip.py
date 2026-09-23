    @deprecate_renamed_function("strip_chars", version="0.19.3")
    def strip(self, characters: str | None = None) -> Expr:
        """
        Remove leading and trailing characters.

        .. deprecated:: 0.19.3
            This method has been renamed to :func:`strip_chars`.

        Parameters
        ----------
        characters
            The set of characters to be removed. All combinations of this set of
            characters will be stripped. If set to None (default), all whitespace is
            removed instead.
        """
        return self.strip_chars(characters)
