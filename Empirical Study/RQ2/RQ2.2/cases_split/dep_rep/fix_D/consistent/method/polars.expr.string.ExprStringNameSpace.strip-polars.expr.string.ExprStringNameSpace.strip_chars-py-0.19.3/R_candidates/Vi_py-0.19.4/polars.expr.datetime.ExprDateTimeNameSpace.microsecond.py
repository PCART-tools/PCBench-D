    def microsecond(self) -> Expr:
        """
        Extract microseconds from underlying DateTime representation.

        Applies to Datetime columns.

        Returns
        -------
        Expr
            Expression of data type :class:`UInt32`.

        Examples
        --------
        >>> from datetime import datetime
        >>> df = pl.DataFrame(
        ...     {
        ...         "date": pl.datetime_range(
        ...             datetime(2020, 1, 1),
        ...             datetime(2020, 1, 1, 0, 0, 1, 0),
        ...             "1ms",
        ...             eager=True,
        ...         ),
        ...     }
        ... )
        >>> df.select(
        ...     [
        ...         pl.col("date"),
        ...         pl.col("date").dt.microsecond().alias("microseconds"),
        ...     ]
        ... )
        shape: (1_001, 2)
        ┌─────────────────────────┬──────────────┐
        │ date                    ┆ microseconds │
        │ ---                     ┆ ---          │
        │ datetime[μs]            ┆ u32          │
        ╞═════════════════════════╪══════════════╡
        │ 2020-01-01 00:00:00     ┆ 0            │
        │ 2020-01-01 00:00:00.001 ┆ 1000         │
        │ 2020-01-01 00:00:00.002 ┆ 2000         │
        │ 2020-01-01 00:00:00.003 ┆ 3000         │
        │ …                       ┆ …            │
        │ 2020-01-01 00:00:00.997 ┆ 997000       │
        │ 2020-01-01 00:00:00.998 ┆ 998000       │
        │ 2020-01-01 00:00:00.999 ┆ 999000       │
        │ 2020-01-01 00:00:01     ┆ 0            │
        └─────────────────────────┴──────────────┘

        """
        return wrap_expr(self._pyexpr.dt_microsecond())
