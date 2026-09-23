    def to_datetime(
        self,
        format: str | None = None,
        *,
        time_unit: TimeUnit | None = None,
        time_zone: str | None = None,
        strict: bool = True,
        exact: bool = True,
        cache: bool = True,
        utc: bool | None = None,
        use_earliest: bool | None = None,
        ambiguous: Ambiguous | Series = "raise",
    ) -> Series:
        """
        Convert a String column into a Datetime column.

        Parameters
        ----------
        format
            Format to use for conversion. Refer to the `chrono crate documentation
            <https://docs.rs/chrono/latest/chrono/format/strftime/index.html>`_
            for the full specification. Example: `"%Y-%m-%d %H:%M:%S"`.
            If set to None (default), the format is inferred from the data.
        time_unit : {None, 'us', 'ns', 'ms'}
            Unit of time for the resulting Datetime column. If set to None (default),
            the time unit is inferred from the format string if given, eg:
            `"%F %T%.3f"` => `Datetime("ms")`. If no fractional second component is
            found, the default is `"us"`.
        time_zone
            Time zone for the resulting Datetime column.
        strict
            Raise an error if any conversion fails.
        exact
            Require an exact format match. If False, allow the format to match anywhere
            in the target string.

            .. note::
                Using `exact=False` introduces a performance penalty - cleaning your
                data beforehand will almost certainly be more performant.
        cache
            Use a cache of unique, converted datetimes to apply the conversion.
        utc
            Parse time zone aware datetimes as UTC. This may be useful if you have data
            with mixed offsets.

            .. deprecated:: 0.18.0
                This is now a no-op, you can safely remove it.
                Offset-naive strings are parsed as `pl.Datetime(time_unit)`,
                and offset-aware strings are converted to
                `pl.Datetime(time_unit, "UTC")`.
        use_earliest
            Determine how to deal with ambiguous datetimes:

            - `None` (default): raise
            - `True`: use the earliest datetime
            - `False`: use the latest datetime

            .. deprecated:: 0.19.0
                Use `ambiguous` instead
        ambiguous
            Determine how to deal with ambiguous datetimes:

            - `'raise'` (default): raise
            - `'earliest'`: use the earliest datetime
            - `'latest'`: use the latest datetime
            - `'null'`: set to null

        Examples
        --------
        >>> s = pl.Series(["2020-01-01 01:00Z", "2020-01-01 02:00Z"])
        >>> s.str.to_datetime("%Y-%m-%d %H:%M%#z")
        shape: (2,)
        Series: '' [datetime[μs, UTC]]
        [
                2020-01-01 01:00:00 UTC
                2020-01-01 02:00:00 UTC
        ]
        """
