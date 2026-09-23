    @deprecate_function(
        "Instead, first cast to `Int64` and then cast to the desired data type.",
        version="0.20.5",
    )
    def with_time_unit(self, time_unit: TimeUnit) -> Expr:
        """
        Set time unit of an expression of dtype Datetime or Duration.

        .. deprecated:: 0.20.5
            First cast to `Int64` and then cast to the desired data type.

        This does not modify underlying data, and should be used to fix an incorrect
        time unit.

        Parameters
        ----------
        time_unit : {'ns', 'us', 'ms'}
            Unit of time for the `Datetime` or `Duration` expression.

        Examples
        --------
        >>> from datetime import datetime
        >>> df = pl.DataFrame(
        ...     {
        ...         "date": pl.datetime_range(
        ...             datetime(2001, 1, 1),
        ...             datetime(2001, 1, 3),
        ...             "1d",
        ...             time_unit="ns",
        ...             eager=True,
        ...         )
        ...     }
        ... )
        >>> df.select(
        ...     pl.col("date"),
        ...     pl.col("date").dt.with_time_unit("us").alias("time_unit_us"),
        ... )  # doctest: +SKIP
        shape: (3, 2)
        ┌─────────────────────┬───────────────────────┐
        │ date                ┆ time_unit_us          │
        │ ---                 ┆ ---                   │
        │ datetime[ns]        ┆ datetime[μs]          │
        ╞═════════════════════╪═══════════════════════╡
        │ 2001-01-01 00:00:00 ┆ +32971-04-28 00:00:00 │
        │ 2001-01-02 00:00:00 ┆ +32974-01-22 00:00:00 │
        │ 2001-01-03 00:00:00 ┆ +32976-10-18 00:00:00 │
        └─────────────────────┴───────────────────────┘
        """
        return wrap_expr(self._pyexpr.dt_with_time_unit(time_unit))
