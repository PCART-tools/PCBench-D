    def time(self) -> Expr:
        """
        Extract time.

        Applies to Datetime columns only; fails on Date.

        Returns
        -------
        Expr
            Expression of data type :class:`Time`.

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
        >>> df.with_columns(pl.col("datetime").dt.time().alias("time"))
        shape: (3, 2)
        ┌─────────────────────────┬──────────────┐
        │ datetime                ┆ time         │
        │ ---                     ┆ ---          │
        │ datetime[μs]            ┆ time         │
        ╞═════════════════════════╪══════════════╡
        │ 1978-01-01 01:01:01     ┆ 01:01:01     │
        │ 2024-10-13 05:30:14.500 ┆ 05:30:14.500 │
        │ 2065-01-01 10:20:30.060 ┆ 10:20:30.060 │
        └─────────────────────────┴──────────────┘
        """
        return wrap_expr(self._pyexpr.dt_time())
