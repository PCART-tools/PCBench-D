    def year(self) -> Expr:
        """
        Extract year from underlying Date representation.

        Applies to Date and Datetime columns.

        Returns the year number in the calendar date.

        Returns
        -------
        Expr
            Expression of data type :class:`Int32`.

        Examples
        --------
        >>> from datetime import date
        >>> df = pl.DataFrame(
        ...     {"date": [date(1977, 1, 1), date(1978, 1, 1), date(1979, 1, 1)]}
        ... )
        >>> df.with_columns(
        ...     calendar_year=pl.col("date").dt.year(),
        ...     iso_year=pl.col("date").dt.iso_year(),
        ... )
        shape: (3, 3)
        ┌────────────┬───────────────┬──────────┐
        │ date       ┆ calendar_year ┆ iso_year │
        │ ---        ┆ ---           ┆ ---      │
        │ date       ┆ i32           ┆ i32      │
        ╞════════════╪═══════════════╪══════════╡
        │ 1977-01-01 ┆ 1977          ┆ 1976     │
        │ 1978-01-01 ┆ 1978          ┆ 1977     │
        │ 1979-01-01 ┆ 1979          ┆ 1979     │
        └────────────┴───────────────┴──────────┘
        """
        return wrap_expr(self._pyexpr.dt_year())
