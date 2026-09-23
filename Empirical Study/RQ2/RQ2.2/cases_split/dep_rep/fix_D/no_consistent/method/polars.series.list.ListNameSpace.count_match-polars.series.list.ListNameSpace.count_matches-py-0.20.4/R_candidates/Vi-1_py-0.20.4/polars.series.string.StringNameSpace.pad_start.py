    def pad_start(self, length: int, fill_char: str = " ") -> Series:
        """
        Pad the start of the string until it reaches the given length.

        Parameters
        ----------
        length
            Pad the string until it reaches this length. Strings with length equal to
            or greater than this value are returned as-is.
        fill_char
            The character to pad the string with.

        See Also
        --------
        pad_end
        zfill

        Examples
        --------
        >>> s = pl.Series("a", ["cow", "monkey", "hippopotamus", None])
        >>> s.str.pad_start(8, "*")
        shape: (4,)
        Series: 'a' [str]
        [
            "*****cow"
            "**monkey"
            "hippopotamus"
            null
        ]
        """
