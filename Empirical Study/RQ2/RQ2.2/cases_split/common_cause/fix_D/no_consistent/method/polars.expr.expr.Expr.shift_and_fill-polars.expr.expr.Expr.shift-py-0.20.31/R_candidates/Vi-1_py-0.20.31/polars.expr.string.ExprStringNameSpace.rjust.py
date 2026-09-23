    @deprecate_renamed_function("pad_start", version="0.19.12")
    @deprecate_renamed_parameter("width", "length", version="0.19.12")
    def rjust(self, length: int, fill_char: str = " ") -> Expr:
        """
        Return the string right justified in a string of length `length`.

        .. deprecated:: 0.19.12
            This method has been renamed to :func:`pad_start`.

        Parameters
        ----------
        length
            Justify right to this length.
        fill_char
            Fill with this ASCII character.
        """
        return self.pad_start(length, fill_char)
