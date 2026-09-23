    def join(self, delimiter: str = "", *, ignore_nulls: bool = True) -> Series:
        """
        Vertically concatenate the string values in the column to a single string value.

        Parameters
        ----------
        delimiter
            The delimiter to insert between consecutive string values.
        ignore_nulls
            Ignore null values (default).
            If set to `False`, null values will be propagated. This means that
            if the column contains any null values, the output is null.

        Returns
        -------
        Series
            Series of data type :class:`String`.

        Examples
        --------
        >>> s = pl.Series([1, None, 3])
        >>> s.str.join("-")
        shape: (1,)
        Series: '' [str]
        [
            "1-3"
        ]
        >>> s.str.join(ignore_nulls=False)
        shape: (1,)
        Series: '' [str]
        [
            null
        ]
        """
