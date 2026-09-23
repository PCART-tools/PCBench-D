    def combine(self, time: dt.time | Series, time_unit: TimeUnit = "us") -> Expr:
        """
        Create a naive Datetime from an existing Date/Datetime expression and a Time.

        If the underlying expression is a Datetime then its time component is replaced,
        and if it is a Date then a new Datetime is created by combining the two values.

        Parameters
        ----------
        time
            A python time literal or Series of the same length as this Series.
        time_unit : {'ns', 'us', 'ms'}
            Unit of time.

        Examples
        --------
        >>> from datetime import datetime, time
        >>> s = pl.Series(
        ...     "dtm",
        ...     [datetime(2022, 12, 31, 10, 30, 45), datetime(2023, 7, 5, 23, 59, 59)],
        ... )
        >>> s.dt.combine(time(1, 2, 3, 456000))
        shape: (2,)
        Series: 'dtm' [datetime[μs]]
        [
            2022-12-31 01:02:03.456
            2023-07-05 01:02:03.456
        ]
        """
