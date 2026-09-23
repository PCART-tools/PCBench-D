    def timestamp(self, time_unit: TimeUnit = "us") -> Expr:
        """
        Return a timestamp in the given time unit.

        Parameters
        ----------
        time_unit : {'ns', 'us', 'ms'}
            Time unit.

        Examples
        --------
        >>> from datetime import date
        >>> df = (
        ...     pl.date_range(date(2001, 1, 1), date(2001, 1, 3), eager=True)
        ...     .alias("date")
        ...     .to_frame()
        ... )
        >>> df.with_columns(
        ...     pl.col("date").dt.timestamp().alias("timestamp_us"),
        ...     pl.col("date").dt.timestamp("ms").alias("timestamp_ms"),
        ... )
        shape: (3, 3)
        ┌────────────┬─────────────────┬──────────────┐
        │ date       ┆ timestamp_us    ┆ timestamp_ms │
        │ ---        ┆ ---             ┆ ---          │
        │ date       ┆ i64             ┆ i64          │
        ╞════════════╪═════════════════╪══════════════╡
        │ 2001-01-01 ┆ 978307200000000 ┆ 978307200000 │
        │ 2001-01-02 ┆ 978393600000000 ┆ 978393600000 │
        │ 2001-01-03 ┆ 978480000000000 ┆ 978480000000 │
        └────────────┴─────────────────┴──────────────┘
        """
        return wrap_expr(self._pyexpr.dt_timestamp(time_unit))
