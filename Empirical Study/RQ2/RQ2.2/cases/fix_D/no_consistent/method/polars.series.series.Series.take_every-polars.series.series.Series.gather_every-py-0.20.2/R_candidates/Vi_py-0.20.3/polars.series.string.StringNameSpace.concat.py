    def concat(self, delimiter: str = "-", *, ignore_nulls: bool = True) -> Series:
        """
        Vertically concat the values in the Series to a single string value.

        Parameters
        ----------
        delimiter
            The delimiter to insert between consecutive string values.
        ignore_nulls
            Ignore null values (default).

            If set to ``False``, null values will be propagated.
            if the column contains any null values, the output is ``None``.

        Returns
        -------
        Series
            Series of data type :class:`String`.

        Examples
        --------
        >>> pl.Series([1, None, 2]).str.concat("-")
        shape: (1,)
        Series: '' [str]
        [
            "1-2"
        ]
        >>> pl.Series([1, None, 2]).str.concat("-", ignore_nulls=False)
        shape: (1,)
        Series: '' [str]
        [
            null
        ]

        """
