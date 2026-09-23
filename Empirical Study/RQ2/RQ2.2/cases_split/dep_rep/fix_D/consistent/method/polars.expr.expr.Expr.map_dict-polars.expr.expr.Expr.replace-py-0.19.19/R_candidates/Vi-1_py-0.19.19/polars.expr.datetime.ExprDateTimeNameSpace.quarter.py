    def quarter(self) -> Expr:
        """
        Extract quarter from underlying Date representation.

        Applies to Date and Datetime columns.

        Returns the quarter ranging from 1 to 4.

        Returns
        -------
        Expr
            Expression of data type :class:`UInt32`.

        Examples
        --------
        >>> from datetime import date
        >>> df = pl.DataFrame(
        ...     {"date": [date(2001, 1, 1), date(2001, 6, 30), date(2001, 12, 27)]}
        ... )
        >>> df.with_columns(pl.col("date").dt.quarter().alias("quarter"))
        shape: (3, 2)
        ┌────────────┬─────────┐
        │ date       ┆ quarter │
        │ ---        ┆ ---     │
        │ date       ┆ u32     │
        ╞════════════╪═════════╡
        │ 2001-01-01 ┆ 1       │
        │ 2001-06-30 ┆ 2       │
        │ 2001-12-27 ┆ 4       │
        └────────────┴─────────┘

        """
        return wrap_expr(self._pyexpr.dt_quarter())
