    def len_bytes(self) -> Series:
        """
        Return the length of each string as the number of bytes.

        Returns
        -------
        Series
            Series of data type :class:`UInt32`.

        See Also
        --------
        len_chars

        Notes
        -----
        When working with non-ASCII text, the length in bytes is not the same as the
        length in characters. You may want to use :func:`len_chars` instead.
        Note that :func:`len_bytes` is much more performant (_O(1)_) than
        :func:`len_chars` (_O(n)_).

        Examples
        --------
        >>> s = pl.Series(["Café", "345", "東京", None])
        >>> s.str.len_bytes()
        shape: (4,)
        Series: '' [u32]
        [
            5
            3
            6
            null
        ]
        """
