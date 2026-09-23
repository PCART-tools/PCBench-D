    def is_leap_year(self) -> Expr:
        """
        Determine whether the year of the underlying date is a leap year.

        Applies to Date and Datetime columns.

        Returns
        -------
        Expr
            Expression of data type :class:`Boolean`.

        Examples
        --------
        >>> from datetime import date
        >>> df = pl.DataFrame(
        ...     {"date": [date(2000, 1, 1), date(2001, 1, 1), date(2002, 1, 1)]}
        ... )
        >>> df.with_columns(
        ...     leap_year=pl.col("date").dt.is_leap_year(),
        ... )
        shape: (3, 2)
        ┌────────────┬───────────┐
        │ date       ┆ leap_year │
        │ ---        ┆ ---       │
        │ date       ┆ bool      │
        ╞════════════╪═══════════╡
        │ 2000-01-01 ┆ true      │
        │ 2001-01-01 ┆ false     │
        │ 2002-01-01 ┆ false     │
        └────────────┴───────────┘
        """
        return wrap_expr(self._pyexpr.dt_is_leap_year())
