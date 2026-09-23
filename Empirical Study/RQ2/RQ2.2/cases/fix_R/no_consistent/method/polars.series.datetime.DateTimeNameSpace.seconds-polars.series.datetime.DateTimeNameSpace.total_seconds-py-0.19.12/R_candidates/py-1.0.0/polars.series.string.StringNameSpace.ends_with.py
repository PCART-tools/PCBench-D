    def ends_with(self, suffix: str | Expr) -> Series:
        """
        Check if string values end with a substring.

        Parameters
        ----------
        suffix
            Suffix substring.

        See Also
        --------
        contains : Check if string contains a substring that matches a regex.
        starts_with : Check if string values start with a substring.

        Examples
        --------
        >>> s = pl.Series("fruits", ["apple", "mango", None])
        >>> s.str.ends_with("go")
        shape: (3,)
        Series: 'fruits' [bool]
        [
            false
            true
            null
        ]
        """
