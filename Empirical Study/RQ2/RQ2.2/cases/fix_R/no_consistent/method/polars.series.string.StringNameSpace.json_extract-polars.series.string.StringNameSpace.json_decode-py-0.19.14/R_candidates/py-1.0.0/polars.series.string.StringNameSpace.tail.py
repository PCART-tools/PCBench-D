    def tail(self, n: int | IntoExprColumn) -> Series:
        """
        Return the last n characters of each string in a String Series.

        Parameters
        ----------
        n
            Length of the slice (integer or expression). Negative indexing is supported;
            see note (2) below.

        Returns
        -------
        Series
            Series of data type :class:`String`.

        Notes
        -----
        1) The `n` input is defined in terms of the number of characters in the (UTF8)
           string. A character is defined as a `Unicode scalar value`_. A single
           character is represented by a single byte when working with ASCII text, and a
           maximum of 4 bytes otherwise.

           .. _Unicode scalar value: https://www.unicode.org/glossary/#unicode_scalar_value

        2) When `n` is negative, `tail` returns characters starting from the `n`th from
           the beginning of the string. For example, if `n = -3`, then all characters
           except the first three are returned.

        3) If the length of the string has fewer than `n` characters, the full string is
           returned.

        Examples
        --------
        Return up to the last 5 characters:

        >>> s = pl.Series(["pear", None, "papaya", "dragonfruit"])
        >>> s.str.tail(5)
        shape: (4,)
        Series: '' [str]
        [
            "pear"
            null
            "apaya"
            "fruit"
        ]

        Return from the 3rd character to the end:

        >>> s = pl.Series(["pear", None, "papaya", "dragonfruit"])
        >>> s.str.tail(-3)
        shape: (4,)
        Series: '' [str]
        [
            "r"
            null
            "aya"
            "gonfruit"
        ]
        """
