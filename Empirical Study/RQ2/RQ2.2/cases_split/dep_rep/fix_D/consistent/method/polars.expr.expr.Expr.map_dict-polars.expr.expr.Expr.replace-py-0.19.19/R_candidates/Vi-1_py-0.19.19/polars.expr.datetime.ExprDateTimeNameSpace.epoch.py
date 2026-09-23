    def epoch(self, time_unit: EpochTimeUnit = "us") -> Expr:
        """
        Get the time passed since the Unix EPOCH in the give time unit.

        Parameters
        ----------
        time_unit : {'ns', 'us', 'ms', 's', 'd'}
            Time unit.

        Examples
        --------
        >>> from datetime import date
        >>> df = pl.date_range(
        ...     date(2001, 1, 1), date(2001, 1, 3), eager=True
        ... ).to_frame()
        >>> df.with_columns(
        ...     pl.col("date").dt.epoch().alias("epoch_ns"),
        ...     pl.col("date").dt.epoch(time_unit="s").alias("epoch_s"),
        ... )
        shape: (3, 3)
        ┌────────────┬─────────────────┬───────────┐
        │ date       ┆ epoch_ns        ┆ epoch_s   │
        │ ---        ┆ ---             ┆ ---       │
        │ date       ┆ i64             ┆ i64       │
        ╞════════════╪═════════════════╪═══════════╡
        │ 2001-01-01 ┆ 978307200000000 ┆ 978307200 │
        │ 2001-01-02 ┆ 978393600000000 ┆ 978393600 │
        │ 2001-01-03 ┆ 978480000000000 ┆ 978480000 │
        └────────────┴─────────────────┴───────────┘

        """
        if time_unit in DTYPE_TEMPORAL_UNITS:
            return self.timestamp(time_unit)  # type: ignore[arg-type]
        elif time_unit == "s":
            return wrap_expr(self._pyexpr.dt_epoch_seconds())
        elif time_unit == "d":
            return wrap_expr(self._pyexpr).cast(Date).cast(Int32)
        else:
            raise ValueError(
                f"`time_unit` must be one of {{'ns', 'us', 'ms', 's', 'd'}}, got {time_unit!r}"
            )
