    def strip_suffix(self, suffix: IntoExpr) -> Series:
        """
        Remove suffix.

        The suffix will be removed from the string exactly once, if found.

        Parameters
        ----------
        suffix
            The suffix to be removed.

        Examples
        --------
        >>> s = pl.Series(["foobar", "foobarbar", "foo", "bar"])
        >>> s.str.strip_suffix("bar")
        shape: (4,)
        Series: '' [str]
        [
                "foo"
                "foobar"
                "foo"
                ""
        ]
        """
