    def pad_end(self, length: int, fill_char: str = " ") -> Series:
        """
        Pad the end of the string until it reaches the given length.

        Parameters
        ----------
        length
            Pad the string until it reaches this length. Strings with length equal to
            or greater than this value are returned as-is.
        fill_char
            The character to pad the string with.

        See Also
        --------
        pad_start

        Examples
        --------
        >>> s = pl.Series(["cow", "monkey", "hippopotamus", None])
        >>> s.str.pad_end(8, "*")
        shape: (4,)
        Series: '' [str]
        [
            "cow*****"
            "monkey**"
            "hippopotamus"
            null
        ]

        """
