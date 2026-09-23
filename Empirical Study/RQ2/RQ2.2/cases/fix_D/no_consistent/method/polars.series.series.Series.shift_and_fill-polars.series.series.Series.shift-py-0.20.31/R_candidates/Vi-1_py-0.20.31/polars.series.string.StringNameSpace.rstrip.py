    @deprecate_renamed_function("strip_chars_end", version="0.19.3")
    def rstrip(self, characters: str | None = None) -> Series:
        """
        Remove trailing characters.

        .. deprecated:: 0.19.3
            This method has been renamed to :func:`Series.strip_chars_end`.

        Parameters
        ----------
        characters
            The set of characters to be removed. All combinations of this set of
            characters will be stripped. If set to None (default), all whitespace is
            removed instead.
        """
