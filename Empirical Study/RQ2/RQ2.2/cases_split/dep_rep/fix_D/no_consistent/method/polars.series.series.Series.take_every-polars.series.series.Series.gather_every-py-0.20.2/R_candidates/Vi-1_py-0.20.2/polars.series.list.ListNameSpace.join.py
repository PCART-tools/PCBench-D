    def join(self, separator: IntoExpr) -> Series:
        """
        Join all string items in a sublist and place a separator between them.

        This errors if inner type of list `!= Utf8`.

        Parameters
        ----------
        separator
            string to separate the items with

        Returns
        -------
        Series
            Series of data type :class:`Utf8`.

        Examples
        --------
        >>> s = pl.Series([["foo", "bar"], ["hello", "world"]])
        >>> s.list.join(separator="-")
        shape: (2,)
        Series: '' [str]
        [
            "foo-bar"
            "hello-world"
        ]

        """
