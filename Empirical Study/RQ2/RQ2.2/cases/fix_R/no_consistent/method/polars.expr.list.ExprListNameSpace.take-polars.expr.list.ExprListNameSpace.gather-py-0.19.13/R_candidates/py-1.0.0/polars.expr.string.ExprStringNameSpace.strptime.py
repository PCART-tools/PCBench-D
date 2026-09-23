    def strptime(
        self,
        dtype: PolarsTemporalType,
        format: str | None = None,
        *,
        strict: bool = True,
        exact: bool = True,
        cache: bool = True,
        ambiguous: Ambiguous | Expr = "raise",
    ) -> Expr:
        """
        Convert a String column into a Date/Datetime/Time column.

        Parameters
        ----------
        dtype
            The data type to convert into. Can be either Date, Datetime, or Time.
        format
            Format to use for conversion. Refer to the `chrono crate documentation
            <https://docs.rs/chrono/latest/chrono/format/strftime/index.html>`_
            for the full specification. Example: `"%Y-%m-%d %H:%M:%S"`.
            If set to None (default), the format is inferred from the data.
        strict
            Raise an error if any conversion fails.
        exact
            Require an exact format match. If False, allow the format to match anywhere
            in the target string. Conversion to the Time type is always exact.

            .. note::
                Using `exact=False` introduces a performance penalty - cleaning your
                data beforehand will almost certainly be more performant.
        cache
            Use a cache of unique, converted dates to apply the datetime conversion.
        ambiguous
            Determine how to deal with ambiguous datetimes:

            - `'raise'` (default): raise
            - `'earliest'`: use the earliest datetime
            - `'latest'`: use the latest datetime
            - `'null'`: set to null

        Notes
        -----
        When converting to a Datetime type, the time unit is inferred from the format
        string if given, eg: `"%F %T%.3f"` => `Datetime("ms")`. If no fractional
        second component is found, the default is `"us"`.

        Examples
        --------
        Dealing with a consistent format:

        >>> s = pl.Series(["2020-01-01 01:00Z", "2020-01-01 02:00Z"])
        >>> s.str.strptime(pl.Datetime, "%Y-%m-%d %H:%M%#z")
        shape: (2,)
        Series: '' [datetime[μs, UTC]]
        [
                2020-01-01 01:00:00 UTC
                2020-01-01 02:00:00 UTC
        ]

        Dealing with different formats.

        >>> s = pl.Series(
        ...     "date",
        ...     [
        ...         "2021-04-22",
        ...         "2022-01-04 00:00:00",
        ...         "01/31/22",
        ...         "Sun Jul  8 00:34:60 2001",
        ...     ],
        ... )
        >>> s.to_frame().select(
        ...     pl.coalesce(
        ...         pl.col("date").str.strptime(pl.Date, "%F", strict=False),
        ...         pl.col("date").str.strptime(pl.Date, "%F %T", strict=False),
        ...         pl.col("date").str.strptime(pl.Date, "%D", strict=False),
        ...         pl.col("date").str.strptime(pl.Date, "%c", strict=False),
        ...     )
        ... ).to_series()
        shape: (4,)
        Series: 'date' [date]
        [
                2021-04-22
                2022-01-04
                2022-01-31
                2001-07-08
        ]
        """
        if dtype == Date:
            return self.to_date(format, strict=strict, exact=exact, cache=cache)
        elif dtype == Datetime:
            time_unit = getattr(dtype, "time_unit", None)
            time_zone = getattr(dtype, "time_zone", None)
            return self.to_datetime(
                format,
                time_unit=time_unit,
                time_zone=time_zone,
                strict=strict,
                exact=exact,
                cache=cache,
                ambiguous=ambiguous,
            )
        elif dtype == Time:
            return self.to_time(format, strict=strict, cache=cache)
        else:
            msg = "`dtype` must be of type {Date, Datetime, Time}"
            raise ValueError(msg)
