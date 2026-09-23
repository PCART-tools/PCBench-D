    @deprecate_renamed_function("pad_end", version="0.19.12")
    @deprecate_renamed_parameter("width", "length", version="0.19.12")
    def ljust(self, length: int, fill_char: str = " ") -> Expr:
        """
        Return the string left justified in a string of length `length`.

        .. deprecated:: 0.19.12
            This method has been renamed to :func:`pad_end`.

        Parameters
        ----------
        length
            Justify left to this length.
        fill_char
            Fill with this ASCII character.
        """
        return self.pad_end(length, fill_char)
