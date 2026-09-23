    @deprecate_function(
        'Use `.str.split("").explode()` instead.'
        " Note that empty strings will result in null instead of being preserved."
        " To get the exact same behavior, split first and then use when/then/otherwise"
        " to handle the empty list before exploding.",
        version="0.20.31",
    )
    def explode(self) -> Series:
        """
        Returns a column with a separate row for every string character.

        .. deprecated:: 0.20.31
            Use `.str.split("").explode()` instead.
            Note that empty strings will result in null instead of being preserved.
            To get the exact same behavior, split first and then use when/then/otherwise
            to handle the empty list before exploding.

        Returns
        -------
        Series
            Series of data type :class:`String`.

        Examples
        --------
        >>> s = pl.Series("a", ["foo", "bar"])
        >>> s.str.explode()  # doctest: +SKIP
        shape: (6,)
        Series: 'a' [str]
        [
                "f"
                "o"
                "o"
                "b"
                "a"
                "r"
        ]
        """
