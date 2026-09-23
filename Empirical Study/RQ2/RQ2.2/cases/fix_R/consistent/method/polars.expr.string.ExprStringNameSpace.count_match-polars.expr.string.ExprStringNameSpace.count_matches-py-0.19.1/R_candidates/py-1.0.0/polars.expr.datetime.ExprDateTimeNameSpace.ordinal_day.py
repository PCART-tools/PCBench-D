    def ordinal_day(self) -> Expr:
        """
        Extract ordinal day from underlying Date representation.

        Applies to Date and Datetime columns.

        Returns the day of year starting from 1.
        The return value ranges from 1 to 366. (The last day of year differs by years.)

        Returns
        -------
        Expr
            Expression of data type :class:`Int16`.

        See Also
        --------
        weekday
        day

        Examples
        --------
        >>> from datetime import date
        >>> df = pl.DataFrame(
        ...     {
        ...         "date": pl.date_range(
        ...             date(2001, 12, 22), date(2001, 12, 25), eager=True
        ...         )
        ...     }
        ... )
        >>> df.with_columns(
        ...     pl.col("date").dt.weekday().alias("weekday"),
        ...     pl.col("date").dt.day().alias("day_of_month"),
        ...     pl.col("date").dt.ordinal_day().alias("day_of_year"),
        ... )
        shape: (4, 4)
        ┌────────────┬─────────┬──────────────┬─────────────┐
        │ date       ┆ weekday ┆ day_of_month ┆ day_of_year │
        │ ---        ┆ ---     ┆ ---          ┆ ---         │
        │ date       ┆ i8      ┆ i8           ┆ i16         │
        ╞════════════╪═════════╪══════════════╪═════════════╡
        │ 2001-12-22 ┆ 6       ┆ 22           ┆ 356         │
        │ 2001-12-23 ┆ 7       ┆ 23           ┆ 357         │
        │ 2001-12-24 ┆ 1       ┆ 24           ┆ 358         │
        │ 2001-12-25 ┆ 2       ┆ 25           ┆ 359         │
        └────────────┴─────────┴──────────────┴─────────────┘
        """
        return wrap_expr(self._pyexpr.dt_ordinal_day())
