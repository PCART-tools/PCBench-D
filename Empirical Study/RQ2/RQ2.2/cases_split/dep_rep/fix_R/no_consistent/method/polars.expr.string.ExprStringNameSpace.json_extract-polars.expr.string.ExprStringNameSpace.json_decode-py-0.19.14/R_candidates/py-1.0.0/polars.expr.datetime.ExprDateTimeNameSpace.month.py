    def month(self) -> Expr:
        """
        Extract month from underlying Date representation.

        Applies to Date and Datetime columns.

        Returns the month number starting from 1.
        The return value ranges from 1 to 12.

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
        >>> df.with_columns(pl.col("date").dt.month().alias("month"))
        shape: (3, 2)
        ┌────────────┬───────┐
        │ date       ┆ month │
        │ ---        ┆ ---   │
        │ date       ┆ i8    │
        ╞════════════╪═══════╡
        │ 2001-01-01 ┆ 1     │
        │ 2001-06-30 ┆ 6     │
        │ 2001-12-27 ┆ 12    │
        └────────────┴───────┘
        """
        return wrap_expr(self._pyexpr.dt_month())
