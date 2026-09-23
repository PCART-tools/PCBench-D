    def date(self) -> Expr:
        """
        Extract date from date(time).

        Applies to Date and Datetime columns.

        Returns
        -------
        Expr
            Expression of data type :class:`Date`.

        Examples
        --------
        >>> from datetime import datetime
        >>> df = pl.DataFrame(
        ...     {
        ...         "datetime": [
        ...             datetime(1978, 1, 1, 1, 1, 1, 0),
        ...             datetime(2024, 10, 13, 5, 30, 14, 500_000),
        ...             datetime(2065, 1, 1, 10, 20, 30, 60_000),
        ...         ]
        ...     }
        ... )
        >>> df.with_columns(pl.col("datetime").dt.date().alias("date"))
        shape: (3, 2)
        ┌─────────────────────────┬────────────┐
        │ datetime                ┆ date       │
        │ ---                     ┆ ---        │
        │ datetime[μs]            ┆ date       │
        ╞═════════════════════════╪════════════╡
        │ 1978-01-01 01:01:01     ┆ 1978-01-01 │
        │ 2024-10-13 05:30:14.500 ┆ 2024-10-13 │
        │ 2065-01-01 10:20:30.060 ┆ 2065-01-01 │
        └─────────────────────────┴────────────┘
        """
        return wrap_expr(self._pyexpr.dt_date())
