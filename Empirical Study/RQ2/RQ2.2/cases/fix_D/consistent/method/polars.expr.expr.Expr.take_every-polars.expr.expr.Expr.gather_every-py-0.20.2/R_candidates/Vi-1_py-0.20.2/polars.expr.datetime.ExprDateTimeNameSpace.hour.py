    def hour(self) -> Expr:
        """
        Extract hour from underlying DateTime representation.

        Applies to Datetime columns.

        Returns the hour number from 0 to 23.

        Returns
        -------
        Expr
            Expression of data type :class:`Int8`.

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
        >>> df.with_columns(pl.col("datetime").dt.hour().alias("hour"))
        shape: (3, 2)
        ┌─────────────────────┬──────┐
        │ datetime            ┆ hour │
        │ ---                 ┆ ---  │
        │ datetime[μs]        ┆ i8   │
        ╞═════════════════════╪══════╡
        │ 2001-01-01 00:00:00 ┆ 0    │
        │ 2010-01-01 15:30:45 ┆ 15   │
        │ 2022-12-31 23:59:59 ┆ 23   │
        └─────────────────────┴──────┘

        """
        return wrap_expr(self._pyexpr.dt_hour())
