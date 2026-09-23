    def week(self) -> Expr:
        """
        Extract the week from the underlying Date representation.

        Applies to Date and Datetime columns.

        Returns the ISO week number starting from 1.
        The return value ranges from 1 to 53. (The last week of year differs by years.)

        Returns
        -------
        Expr
            Expression of data type :class:`Int8`.

        Examples
        --------
        >>> from datetime import date
        >>> df = pl.DataFrame(
        ...     {"date": [date(2001, 1, 1), date(2001, 6, 30), date(2001, 12, 27)]}
        ... )
        >>> df.with_columns(pl.col("date").dt.week().alias("week"))
        shape: (3, 2)
        ┌────────────┬──────┐
        │ date       ┆ week │
        │ ---        ┆ ---  │
        │ date       ┆ i8   │
        ╞════════════╪══════╡
        │ 2001-01-01 ┆ 1    │
        │ 2001-06-30 ┆ 26   │
        │ 2001-12-27 ┆ 52   │
        └────────────┴──────┘
        """
        return wrap_expr(self._pyexpr.dt_week())
