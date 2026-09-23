    def century(self) -> Expr:
        """
        Extract the century from underlying representation.

        Applies to Date and Datetime columns.

        Returns the century number in the calendar date.

        Returns
        -------
        Expr
            Expression of data type :class:`Int32`.

        Examples
        --------
        >>> from datetime import date
        >>> df = pl.DataFrame(
        ...     {
        ...         "date": [
        ...             date(999, 12, 31),
        ...             date(1897, 5, 7),
        ...             date(2000, 1, 1),
        ...             date(2001, 7, 5),
        ...             date(3002, 10, 20),
        ...         ]
        ...     }
        ... )
        >>> df.with_columns(cent=pl.col("date").dt.century())
        shape: (5, 2)
        ┌────────────┬──────┐
        │ date       ┆ cent │
        │ ---        ┆ ---  │
        │ date       ┆ i32  │
        ╞════════════╪══════╡
        │ 0999-12-31 ┆ 10   │
        │ 1897-05-07 ┆ 19   │
        │ 2000-01-01 ┆ 20   │
        │ 2001-07-05 ┆ 21   │
        │ 3002-10-20 ┆ 31   │
        └────────────┴──────┘
        """
        return wrap_expr(self._pyexpr.dt_century())
