    @deprecate_function(
        "Use `str.join` instead. Note that the default `delimiter` for `str.join`"
        " is an empty string instead of a hyphen.",
        version="1.0.0",
    )
    def concat(
        self, delimiter: str | None = None, *, ignore_nulls: bool = True
    ) -> Series:
        """
        Vertically concatenate the string values in the column to a single string value.

        .. deprecated:: 1.0.0
            Use :meth:`join` instead. Note that the default `delimiter` for :meth:`join`
            is an empty string instead of a hyphen.

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
        >>> pl.Series([1, None, 2]).str.concat("-")  # doctest: +SKIP
        shape: (1,)
        Series: '' [str]
        [
            "1-2"
        ]
        >>> pl.Series([1, None, 2]).str.concat(ignore_nulls=False)  # doctest: +SKIP
        shape: (1,)
        Series: '' [str]
        [
            null
        ]
        """
