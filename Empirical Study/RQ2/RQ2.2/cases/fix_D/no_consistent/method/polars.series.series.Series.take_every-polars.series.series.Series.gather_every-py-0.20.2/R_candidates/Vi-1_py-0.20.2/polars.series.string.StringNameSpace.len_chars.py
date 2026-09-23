    def len_chars(self) -> Series:
        """
        Return the length of each string as the number of characters.

        Returns
        -------
        Series
            Series of data type :class:`UInt32`.

        See Also
        --------
        len_bytes

        Notes
        -----
        When working with ASCII text, use :func:`len_bytes` instead to achieve
        equivalent output with much better performance:
        :func:`len_bytes` runs in _O(1)_, while :func:`len_chars` runs in (_O(n)_).

        Examples
        --------
        >>> s = pl.Series(["Café", "345", "東京", None])
        >>> s.str.len_chars()
        shape: (4,)
        Series: '' [u32]
        [
            4
            3
            2
            null
        ]

        """
