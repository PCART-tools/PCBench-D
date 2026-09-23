    def to_uppercase(self) -> Series:
        """
        Modify the strings to their uppercase equivalent.

        Examples
        --------
        >>> s = pl.Series("foo", ["cat", "dog"])
        >>> s.str.to_uppercase()
        shape: (2,)
        Series: 'foo' [str]
        [
            "CAT"
            "DOG"
        ]

        """
