    def millennium(self) -> Expr:
        """
        Extract the millennium from underlying representation.

        Applies to Date and Datetime columns.

        Returns the millennium number in the calendar date.

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
        >>> df.with_columns(mlnm=pl.col("date").dt.millennium())
        shape: (5, 2)
        ┌────────────┬──────┐
        │ date       ┆ mlnm │
        │ ---        ┆ ---  │
        │ date       ┆ i32  │
        ╞════════════╪══════╡
        │ 0999-12-31 ┆ 1    │
        │ 1897-05-07 ┆ 2    │
        │ 2000-01-01 ┆ 2    │
        │ 2001-07-05 ┆ 3    │
        │ 3002-10-20 ┆ 4    │
        └────────────┴──────┘
        """
        return wrap_expr(self._pyexpr.dt_millennium())
