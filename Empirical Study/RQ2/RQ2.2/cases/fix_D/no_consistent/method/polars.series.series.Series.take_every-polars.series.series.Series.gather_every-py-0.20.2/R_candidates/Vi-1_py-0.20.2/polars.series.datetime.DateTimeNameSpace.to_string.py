    def to_string(self, format: str) -> Series:
        """
        Convert a Date/Time/Datetime column into a Utf8 column with the given format.

        Similar to `cast(pl.Utf8)`, but this method allows you to customize the
        formatting of the resulting string.

        Parameters
        ----------
        format
            Format to use, refer to the `chrono strftime documentation
            <https://docs.rs/chrono/latest/chrono/format/strftime/index.html>`_
            for specification. Example: `"%y-%m-%d"`.

        Examples
        --------
        >>> from datetime import datetime
        >>> s = pl.Series(
        ...     "datetime",
        ...     [datetime(2020, 3, 1), datetime(2020, 4, 1), datetime(2020, 5, 1)],
        ... )
        >>> s.dt.to_string("%Y/%m/%d")
        shape: (3,)
        Series: 'datetime' [str]
        [
            "2020/03/01"
            "2020/04/01"
            "2020/05/01"
        ]

        """
