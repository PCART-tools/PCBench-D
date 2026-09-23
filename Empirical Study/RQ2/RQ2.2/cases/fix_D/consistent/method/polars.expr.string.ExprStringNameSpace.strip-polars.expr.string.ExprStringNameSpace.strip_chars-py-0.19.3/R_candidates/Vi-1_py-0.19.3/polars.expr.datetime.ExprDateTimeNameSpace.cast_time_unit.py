    def cast_time_unit(self, time_unit: TimeUnit) -> Expr:
        """
        Cast the underlying data to another time unit. This may lose precision.

        Parameters
        ----------
        time_unit : {'ns', 'us', 'ms'}
            Time unit for the ``Datetime`` expression.

        Examples
        --------
        >>> from datetime import datetime
        >>> df = pl.DataFrame(
        ...     {
        ...         "date": pl.datetime_range(
        ...             datetime(2001, 1, 1), datetime(2001, 1, 3), "1d", eager=True
        ...         )
        ...     }
        ... )
        >>> df.select(
        ...     [
        ...         pl.col("date"),
        ...         pl.col("date").dt.cast_time_unit("ms").alias("time_unit_ms"),
        ...         pl.col("date").dt.cast_time_unit("ns").alias("time_unit_ns"),
        ...     ]
        ... )
        shape: (3, 3)
        ┌─────────────────────┬─────────────────────┬─────────────────────┐
        │ date                ┆ time_unit_ms        ┆ time_unit_ns        │
        │ ---                 ┆ ---                 ┆ ---                 │
        │ datetime[μs]        ┆ datetime[ms]        ┆ datetime[ns]        │
        ╞═════════════════════╪═════════════════════╪═════════════════════╡
        │ 2001-01-01 00:00:00 ┆ 2001-01-01 00:00:00 ┆ 2001-01-01 00:00:00 │
        │ 2001-01-02 00:00:00 ┆ 2001-01-02 00:00:00 ┆ 2001-01-02 00:00:00 │
        │ 2001-01-03 00:00:00 ┆ 2001-01-03 00:00:00 ┆ 2001-01-03 00:00:00 │
        └─────────────────────┴─────────────────────┴─────────────────────┘

        """
        return wrap_expr(self._pyexpr.dt_cast_time_unit(time_unit))
