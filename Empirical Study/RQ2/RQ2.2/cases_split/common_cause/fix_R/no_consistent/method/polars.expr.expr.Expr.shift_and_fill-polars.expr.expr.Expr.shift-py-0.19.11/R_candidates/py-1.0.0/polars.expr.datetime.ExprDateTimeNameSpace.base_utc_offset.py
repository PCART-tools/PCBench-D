    def base_utc_offset(self) -> Expr:
        """
        Base offset from UTC.

        This is usually constant for all datetimes in a given time zone, but
        may vary in the rare case that a country switches time zone, like
        Samoa (Apia) did at the end of 2011.

        Returns
        -------
        Expr
            Expression of data type :class:`Duration`.

        See Also
        --------
        Expr.dt.dst_offset : Daylight savings offset from UTC.

        Examples
        --------
        >>> from datetime import datetime
        >>> df = pl.DataFrame(
        ...     {
        ...         "ts": [datetime(2011, 12, 29), datetime(2012, 1, 1)],
        ...     }
        ... )
        >>> df = df.with_columns(pl.col("ts").dt.replace_time_zone("Pacific/Apia"))
        >>> df.with_columns(pl.col("ts").dt.base_utc_offset().alias("base_utc_offset"))
        shape: (2, 2)
        ┌────────────────────────────┬─────────────────┐
        │ ts                         ┆ base_utc_offset │
        │ ---                        ┆ ---             │
        │ datetime[μs, Pacific/Apia] ┆ duration[ms]    │
        ╞════════════════════════════╪═════════════════╡
        │ 2011-12-29 00:00:00 -10    ┆ -11h            │
        │ 2012-01-01 00:00:00 +14    ┆ 13h             │
        └────────────────────────────┴─────────────────┘
        """
        return wrap_expr(self._pyexpr.dt_base_utc_offset())
