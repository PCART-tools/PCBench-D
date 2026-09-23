    def minute(self) -> Expr:
        """
        Extract minutes from underlying DateTime representation.

        Applies to Datetime columns.

        Returns the minute number from 0 to 59.

        Returns
        -------
        Expr
            Expression of data type :class:`UInt32`.

        Examples
        --------
        >>> from datetime import datetime
        >>> df = pl.DataFrame(
        ...     {
        ...         "datetime": [
        ...             datetime(2001, 1, 1, 0, 0, 0),
        ...             datetime(2010, 1, 1, 15, 30, 45),
        ...             datetime(2022, 12, 31, 23, 59, 59),
        ...         ]
        ...     }
        ... )
        >>> df.with_columns(pl.col("datetime").dt.minute().alias("minute"))
        shape: (3, 2)
        ┌─────────────────────┬────────┐
        │ datetime            ┆ minute │
        │ ---                 ┆ ---    │
        │ datetime[μs]        ┆ u32    │
        ╞═════════════════════╪════════╡
        │ 2001-01-01 00:00:00 ┆ 0      │
        │ 2010-01-01 15:30:45 ┆ 30     │
        │ 2022-12-31 23:59:59 ┆ 59     │
        └─────────────────────┴────────┘

        """
        return wrap_expr(self._pyexpr.dt_minute())
