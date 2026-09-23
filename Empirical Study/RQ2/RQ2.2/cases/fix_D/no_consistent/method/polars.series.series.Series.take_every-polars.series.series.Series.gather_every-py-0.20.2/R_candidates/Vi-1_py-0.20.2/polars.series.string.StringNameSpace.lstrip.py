    @deprecate_renamed_function("strip_chars_start", version="0.19.3")
    def lstrip(self, characters: str | None = None) -> Series:
        """
        Remove leading characters.

        .. deprecated:: 0.19.3
            This method has been renamed to :func:`strip_chars_start`.

        Parameters
        ----------
        characters
            The set of characters to be removed. All combinations of this set of
            characters will be stripped. If set to None (default), all whitespace is
            removed instead.

        """
