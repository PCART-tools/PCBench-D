    @deprecate_function("Use `dt.replace_time_zone(None)` instead.", version="0.20.4")
    def datetime(self) -> Expr:
        """
        Return datetime.

        .. deprecated:: 0.20.4
            Use `dt.replace_time_zone(None)` instead.

        Applies to Datetime columns.

        Returns
        -------
        Expr
            Expression of data type :class:`Datetime`.

        Examples
        --------
        >>> from datetime import datetime
        >>> df = pl.DataFrame(
        ...     {
        ...         "datetime UTC": [
        ...             datetime(1978, 1, 1, 1, 1, 1, 0),
        ...             datetime(2024, 10, 13, 5, 30, 14, 500_000),
        ...             datetime(2065, 1, 1, 10, 20, 30, 60_000),
        ...         ]
        ...     },
        ...     schema={"datetime UTC": pl.Datetime(time_zone="UTC")},
        ... )
        >>> df.with_columns(  # doctest: +SKIP
        ...     pl.col("datetime UTC").dt.datetime().alias("datetime (no timezone)"),
        ... )
        shape: (3, 2)
        ┌─────────────────────────────┬─────────────────────────┐
        │ datetime UTC                ┆ datetime (no timezone)  │
        │ ---                         ┆ ---                     │
        │ datetime[μs, UTC]           ┆ datetime[μs]            │
        ╞═════════════════════════════╪═════════════════════════╡
        │ 1978-01-01 01:01:01 UTC     ┆ 1978-01-01 01:01:01     │
        │ 2024-10-13 05:30:14.500 UTC ┆ 2024-10-13 05:30:14.500 │
        │ 2065-01-01 10:20:30.060 UTC ┆ 2065-01-01 10:20:30.060 │
        └─────────────────────────────┴─────────────────────────┘
        """
        return wrap_expr(self._pyexpr.dt_datetime())
