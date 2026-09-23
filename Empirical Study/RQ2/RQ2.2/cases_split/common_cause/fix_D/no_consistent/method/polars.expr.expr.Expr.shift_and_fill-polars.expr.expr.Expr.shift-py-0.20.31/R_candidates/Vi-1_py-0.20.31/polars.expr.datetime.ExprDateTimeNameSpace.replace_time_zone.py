    def replace_time_zone(
        self,
        time_zone: str | None,
        *,
        use_earliest: bool | None = None,
        ambiguous: Ambiguous | Expr = "raise",
        non_existent: NonExistent = "raise",
    ) -> Expr:
        """
        Replace time zone for an expression of type Datetime.

        Different from `convert_time_zone`, this will also modify
        the underlying timestamp and will ignore the original time zone.

        Parameters
        ----------
        time_zone
            Time zone for the `Datetime` expression. Pass `None` to unset time zone.
        use_earliest
            Determine how to deal with ambiguous datetimes:

            - `None` (default): raise
            - `True`: use the earliest datetime
            - `False`: use the latest datetime

            .. deprecated:: 0.19.0
                Use `ambiguous` instead
        ambiguous
            Determine how to deal with ambiguous datetimes:

            - `'raise'` (default): raise
            - `'earliest'`: use the earliest datetime
            - `'latest'`: use the latest datetime
            - `'null'`: set to null
        non_existent
            Determine how to deal with non-existent datetimes:

            - `'raise'` (default): raise
            - `'null'`: set to null

        Examples
        --------
        >>> from datetime import datetime
        >>> df = pl.DataFrame(
        ...     {
        ...         "london_timezone": pl.datetime_range(
        ...             datetime(2020, 3, 1),
        ...             datetime(2020, 7, 1),
        ...             "1mo",
        ...             time_zone="UTC",
        ...             eager=True,
        ...         ).dt.convert_time_zone(time_zone="Europe/London"),
        ...     }
        ... )
        >>> df.select(
        ...     [
        ...         pl.col("london_timezone"),
        ...         pl.col("london_timezone")
        ...         .dt.replace_time_zone(time_zone="Europe/Amsterdam")
        ...         .alias("London_to_Amsterdam"),
        ...     ]
        ... )
        shape: (5, 2)
        ┌─────────────────────────────┬────────────────────────────────┐
        │ london_timezone             ┆ London_to_Amsterdam            │
        │ ---                         ┆ ---                            │
        │ datetime[μs, Europe/London] ┆ datetime[μs, Europe/Amsterdam] │
        ╞═════════════════════════════╪════════════════════════════════╡
        │ 2020-03-01 00:00:00 GMT     ┆ 2020-03-01 00:00:00 CET        │
        │ 2020-04-01 01:00:00 BST     ┆ 2020-04-01 01:00:00 CEST       │
        │ 2020-05-01 01:00:00 BST     ┆ 2020-05-01 01:00:00 CEST       │
        │ 2020-06-01 01:00:00 BST     ┆ 2020-06-01 01:00:00 CEST       │
        │ 2020-07-01 01:00:00 BST     ┆ 2020-07-01 01:00:00 CEST       │
        └─────────────────────────────┴────────────────────────────────┘

        You can use `ambiguous` to deal with ambiguous datetimes:

        >>> dates = [
        ...     "2018-10-28 01:30",
        ...     "2018-10-28 02:00",
        ...     "2018-10-28 02:30",
        ...     "2018-10-28 02:00",
        ... ]
        >>> df = pl.DataFrame(
        ...     {
        ...         "ts": pl.Series(dates).str.strptime(pl.Datetime),
        ...         "ambiguous": ["earliest", "earliest", "latest", "latest"],
        ...     }
        ... )
        >>> df.with_columns(
        ...     ts_localized=pl.col("ts").dt.replace_time_zone(
        ...         "Europe/Brussels", ambiguous=pl.col("ambiguous")
        ...     )
        ... )
        shape: (4, 3)
        ┌─────────────────────┬───────────┬───────────────────────────────┐
        │ ts                  ┆ ambiguous ┆ ts_localized                  │
        │ ---                 ┆ ---       ┆ ---                           │
        │ datetime[μs]        ┆ str       ┆ datetime[μs, Europe/Brussels] │
        ╞═════════════════════╪═══════════╪═══════════════════════════════╡
        │ 2018-10-28 01:30:00 ┆ earliest  ┆ 2018-10-28 01:30:00 CEST      │
        │ 2018-10-28 02:00:00 ┆ earliest  ┆ 2018-10-28 02:00:00 CEST      │
        │ 2018-10-28 02:30:00 ┆ latest    ┆ 2018-10-28 02:30:00 CET       │
        │ 2018-10-28 02:00:00 ┆ latest    ┆ 2018-10-28 02:00:00 CET       │
        └─────────────────────┴───────────┴───────────────────────────────┘
        """
        ambiguous = rename_use_earliest_to_ambiguous(use_earliest, ambiguous)
        if not isinstance(ambiguous, pl.Expr):
            ambiguous = F.lit(ambiguous)
        return wrap_expr(
            self._pyexpr.dt_replace_time_zone(
                time_zone, ambiguous._pyexpr, non_existent
            )
        )
