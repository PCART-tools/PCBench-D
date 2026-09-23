    def strip_prefix(self, prefix: IntoExpr) -> Series:
        """
        Remove prefix.

        The prefix will be removed from the string exactly once, if found.

        Parameters
        ----------
        prefix
            The prefix to be removed.

        Examples
        --------
        >>> s = pl.Series(["foobar", "foofoobar", "foo", "bar"])
        >>> s.str.strip_prefix("foo")
        shape: (4,)
        Series: '' [str]
        [
                "bar"
                "foobar"
                ""
                "bar"
        ]

        """
