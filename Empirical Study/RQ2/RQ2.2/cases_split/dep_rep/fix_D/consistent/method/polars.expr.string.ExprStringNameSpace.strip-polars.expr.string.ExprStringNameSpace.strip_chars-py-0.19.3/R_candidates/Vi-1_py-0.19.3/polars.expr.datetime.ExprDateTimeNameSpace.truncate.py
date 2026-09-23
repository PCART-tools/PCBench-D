    def truncate(
        self,
        every: str | timedelta,
        offset: str | timedelta | None = None,
        *,
        use_earliest: bool | None = None,
        ambiguous: Ambiguous | Expr = "raise",
    ) -> Expr:
        """
        Divide the date/datetime range into buckets.

        Each date/datetime is mapped to the start of its bucket using the corresponding
        local datetime. Note that weekly buckets start on Monday.

        Parameters
        ----------
        every
            Every interval start and period length
        offset
            Offset the window
        use_earliest
            Determine how to deal with ambiguous datetimes:

            - ``None`` (default): raise
            - ``True``: use the earliest datetime
            - ``False``: use the latest datetime

            .. deprecated:: 0.19.0
                Use `ambiguous` instead
        ambiguous
            Determine how to deal with ambiguous datetimes:

            - ``'raise'`` (default): raise
            - ``'earliest'``: use the earliest datetime
            - ``'latest'``: use the latest datetime

        Notes
        -----
        The ``every`` and ``offset`` argument are created with the
        the following string language:

        - 1ns   (1 nanosecond)
        - 1us   (1 microsecond)
        - 1ms   (1 millisecond)
        - 1s    (1 second)
        - 1m    (1 minute)
        - 1h    (1 hour)
        - 1d    (1 calendar day)
        - 1w    (1 calendar week)
        - 1mo   (1 calendar month)
        - 1q    (1 calendar quarter)
        - 1y    (1 calendar year)

        These strings can be combined:

        - 3d12h4m25s # 3 days, 12 hours, 4 minutes, and 25 seconds

        Suffix with `"_saturating"` to indicate that dates too large for
        their month should saturate at the largest date (e.g. 2022-02-29 -> 2022-02-28)
        instead of erroring.

        By "calendar day", we mean the corresponding time on the next day (which may
        not be 24 hours, due to daylight savings). Similarly for "calendar week",
        "calendar month", "calendar quarter", and "calendar year".

        Returns
        -------
        Expr
            Expression of data type :class:`Date` or :class:`Datetime`.

        Examples
        --------
        >>> from datetime import timedelta, datetime
        >>> df = pl.datetime_range(
        ...     datetime(2001, 1, 1),
        ...     datetime(2001, 1, 2),
        ...     timedelta(minutes=225),
        ...     eager=True,
        ... ).to_frame()
        >>> df
        shape: (7, 1)
        ┌─────────────────────┐
        │ datetime            │
        │ ---                 │
        │ datetime[μs]        │
        ╞═════════════════════╡
        │ 2001-01-01 00:00:00 │
        │ 2001-01-01 03:45:00 │
        │ 2001-01-01 07:30:00 │
        │ 2001-01-01 11:15:00 │
        │ 2001-01-01 15:00:00 │
        │ 2001-01-01 18:45:00 │
        │ 2001-01-01 22:30:00 │
        └─────────────────────┘
        >>> df.select(pl.col("datetime").dt.truncate("1h"))
        shape: (7, 1)
        ┌─────────────────────┐
        │ datetime            │
        │ ---                 │
        │ datetime[μs]        │
        ╞═════════════════════╡
        │ 2001-01-01 00:00:00 │
        │ 2001-01-01 03:00:00 │
        │ 2001-01-01 07:00:00 │
        │ 2001-01-01 11:00:00 │
        │ 2001-01-01 15:00:00 │
        │ 2001-01-01 18:00:00 │
        │ 2001-01-01 22:00:00 │
        └─────────────────────┘
        >>> df.select(pl.col("datetime").dt.truncate("1h")).frame_equal(
        ...     df.select(pl.col("datetime").dt.truncate(timedelta(hours=1)))
        ... )
        True

        >>> df = pl.datetime_range(
        ...     datetime(2001, 1, 1), datetime(2001, 1, 1, 1), "10m", eager=True
        ... ).to_frame()
        >>> df.select(
        ...     "datetime", pl.col("datetime").dt.truncate("30m").alias("truncate")
        ... )
        shape: (7, 2)
        ┌─────────────────────┬─────────────────────┐
        │ datetime            ┆ truncate            │
        │ ---                 ┆ ---                 │
        │ datetime[μs]        ┆ datetime[μs]        │
        ╞═════════════════════╪═════════════════════╡
        │ 2001-01-01 00:00:00 ┆ 2001-01-01 00:00:00 │
        │ 2001-01-01 00:10:00 ┆ 2001-01-01 00:00:00 │
        │ 2001-01-01 00:20:00 ┆ 2001-01-01 00:00:00 │
        │ 2001-01-01 00:30:00 ┆ 2001-01-01 00:30:00 │
        │ 2001-01-01 00:40:00 ┆ 2001-01-01 00:30:00 │
        │ 2001-01-01 00:50:00 ┆ 2001-01-01 00:30:00 │
        │ 2001-01-01 01:00:00 ┆ 2001-01-01 01:00:00 │
        └─────────────────────┴─────────────────────┘

        If crossing daylight savings time boundaries, you may want to use
        `use_earliest` and combine with :func:`~polars.Series.dt.dst_offset`:

        >>> df = (
        ...     pl.datetime_range(
        ...         datetime(2020, 10, 25, 0),
        ...         datetime(2020, 10, 25, 2),
        ...         "30m",
        ...         eager=True,
        ...         time_zone="Europe/London",
        ...     )
        ...     .dt.offset_by("15m")
        ...     .to_frame()
        ... )
        >>> df
        shape: (7, 1)
        ┌─────────────────────────────┐
        │ datetime                    │
        │ ---                         │
        │ datetime[μs, Europe/London] │
        ╞═════════════════════════════╡
        │ 2020-10-25 00:15:00 BST     │
        │ 2020-10-25 00:45:00 BST     │
        │ 2020-10-25 01:15:00 BST     │
        │ 2020-10-25 01:45:00 BST     │
        │ 2020-10-25 01:15:00 GMT     │
        │ 2020-10-25 01:45:00 GMT     │
        │ 2020-10-25 02:15:00 GMT     │
        └─────────────────────────────┘

        >>> ambiguous_mapping = {
        ...     timedelta(hours=1): "earliest",
        ...     timedelta(hours=0): "latest",
        ... }
        >>> df.select(
        ...     pl.col("datetime").dt.truncate(
        ...         "30m",
        ...         ambiguous=(
        ...             pl.col("datetime").dt.dst_offset().map_dict(ambiguous_mapping)
        ...         ),
        ...     )
        ... )
        shape: (7, 1)
        ┌─────────────────────────────┐
        │ datetime                    │
        │ ---                         │
        │ datetime[μs, Europe/London] │
        ╞═════════════════════════════╡
        │ 2020-10-25 00:00:00 BST     │
        │ 2020-10-25 00:30:00 BST     │
        │ 2020-10-25 01:00:00 BST     │
        │ 2020-10-25 01:30:00 BST     │
        │ 2020-10-25 01:00:00 GMT     │
        │ 2020-10-25 01:30:00 GMT     │
        │ 2020-10-25 02:00:00 GMT     │
        └─────────────────────────────┘
        """
        ambiguous = rename_use_earliest_to_ambiguous(use_earliest, ambiguous)
        if not isinstance(ambiguous, pl.Expr):
            ambiguous = F.lit(ambiguous)
        if offset is None:
            offset = "0ns"

        return wrap_expr(
            self._pyexpr.dt_truncate(
                _timedelta_to_pl_duration(every),
                _timedelta_to_pl_duration(offset),
                ambiguous._pyexpr,
            )
        )
