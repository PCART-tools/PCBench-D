    def to_lowercase(self) -> Series:
        """
        Modify the strings to their lowercase equivalent.

        Examples
        --------
        >>> s = pl.Series("foo", ["CAT", "DOG"])
        >>> s.str.to_lowercase()
        shape: (2,)
        Series: 'foo' [str]
        [
            "cat"
            "dog"
        ]

        """
