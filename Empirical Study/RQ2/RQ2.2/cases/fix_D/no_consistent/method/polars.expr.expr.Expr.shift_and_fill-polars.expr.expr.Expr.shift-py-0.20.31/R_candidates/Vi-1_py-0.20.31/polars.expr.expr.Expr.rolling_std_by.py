    @unstable()
    def rolling_std_by(
        self,
        by: IntoExpr,
        window_size: timedelta | str,
        *,
        min_periods: int = 1,
        closed: ClosedInterval = "right",
        ddof: int = 1,
        warn_if_unsorted: bool | None = None,
    ) -> Self:
        """
        Compute a rolling standard deviation based on another column.

        .. warning::
            This functionality is considered **unstable**. It may be changed
            at any point without it being considered a breaking change.

        Given a `by` column `<t_0, t_1, ..., t_n>`, then `closed="right"`
        (the default) means the windows will be:

            - (t_0 - window_size, t_0]
            - (t_1 - window_size, t_1]
            - ...
            - (t_n - window_size, t_n]

        Parameters
        ----------
        by
            This column must be of dtype Datetime or Date.
        window_size
            The length of the window. Can be a dynamic temporal
            size indicated by a timedelta or the following string language:

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

            By "calendar day", we mean the corresponding time on the next day
            (which may not be 24 hours, due to daylight savings). Similarly for
            "calendar week", "calendar month", "calendar quarter", and
            "calendar year".
        min_periods
            The number of values in the window that should be non-null before computing
            a result.
        closed : {'left', 'right', 'both', 'none'}
            Define which sides of the temporal interval are closed (inclusive),
            defaults to `'right'`.
        ddof
            "Delta Degrees of Freedom": The divisor for a length N window is N - ddof
        warn_if_unsorted
            Warn if data is not known to be sorted by `by` column.

            .. deprecated:: 0.20.27
                This operation no longer requires sorted data, you can safely remove
                the `warn_if_unsorted` argument.

        Notes
        -----
        If you want to compute multiple aggregation statistics over the same dynamic
        window, consider using `rolling` - this method can cache the window size
        computation.

        Examples
        --------
        Create a DataFrame with a datetime column and a row number column

        >>> from datetime import timedelta, datetime
        >>> start = datetime(2001, 1, 1)
        >>> stop = datetime(2001, 1, 2)
        >>> df_temporal = pl.DataFrame(
        ...     {"date": pl.datetime_range(start, stop, "1h", eager=True)}
        ... ).with_row_index()
        >>> df_temporal
        shape: (25, 2)
        ┌───────┬─────────────────────┐
        │ index ┆ date                │
        │ ---   ┆ ---                 │
        │ u32   ┆ datetime[μs]        │
        ╞═══════╪═════════════════════╡
        │ 0     ┆ 2001-01-01 00:00:00 │
        │ 1     ┆ 2001-01-01 01:00:00 │
        │ 2     ┆ 2001-01-01 02:00:00 │
        │ 3     ┆ 2001-01-01 03:00:00 │
        │ 4     ┆ 2001-01-01 04:00:00 │
        │ …     ┆ …                   │
        │ 20    ┆ 2001-01-01 20:00:00 │
        │ 21    ┆ 2001-01-01 21:00:00 │
        │ 22    ┆ 2001-01-01 22:00:00 │
        │ 23    ┆ 2001-01-01 23:00:00 │
        │ 24    ┆ 2001-01-02 00:00:00 │
        └───────┴─────────────────────┘

        Compute the rolling std with the temporal windows closed on the right (default)

        >>> df_temporal.with_columns(
        ...     rolling_row_std=pl.col("index").rolling_std_by("date", window_size="2h")
        ... )
        shape: (25, 3)
        ┌───────┬─────────────────────┬─────────────────┐
        │ index ┆ date                ┆ rolling_row_std │
        │ ---   ┆ ---                 ┆ ---             │
        │ u32   ┆ datetime[μs]        ┆ f64             │
        ╞═══════╪═════════════════════╪═════════════════╡
        │ 0     ┆ 2001-01-01 00:00:00 ┆ null            │
        │ 1     ┆ 2001-01-01 01:00:00 ┆ 0.707107        │
        │ 2     ┆ 2001-01-01 02:00:00 ┆ 0.707107        │
        │ 3     ┆ 2001-01-01 03:00:00 ┆ 0.707107        │
        │ 4     ┆ 2001-01-01 04:00:00 ┆ 0.707107        │
        │ …     ┆ …                   ┆ …               │
        │ 20    ┆ 2001-01-01 20:00:00 ┆ 0.707107        │
        │ 21    ┆ 2001-01-01 21:00:00 ┆ 0.707107        │
        │ 22    ┆ 2001-01-01 22:00:00 ┆ 0.707107        │
        │ 23    ┆ 2001-01-01 23:00:00 ┆ 0.707107        │
        │ 24    ┆ 2001-01-02 00:00:00 ┆ 0.707107        │
        └───────┴─────────────────────┴─────────────────┘

        Compute the rolling std with the closure of windows on both sides

        >>> df_temporal.with_columns(
        ...     rolling_row_std=pl.col("index").rolling_std_by(
        ...         "date", window_size="2h", closed="both"
        ...     )
        ... )
        shape: (25, 3)
        ┌───────┬─────────────────────┬─────────────────┐
        │ index ┆ date                ┆ rolling_row_std │
        │ ---   ┆ ---                 ┆ ---             │
        │ u32   ┆ datetime[μs]        ┆ f64             │
        ╞═══════╪═════════════════════╪═════════════════╡
        │ 0     ┆ 2001-01-01 00:00:00 ┆ null            │
        │ 1     ┆ 2001-01-01 01:00:00 ┆ 0.707107        │
        │ 2     ┆ 2001-01-01 02:00:00 ┆ 1.0             │
        │ 3     ┆ 2001-01-01 03:00:00 ┆ 1.0             │
        │ 4     ┆ 2001-01-01 04:00:00 ┆ 1.0             │
        │ …     ┆ …                   ┆ …               │
        │ 20    ┆ 2001-01-01 20:00:00 ┆ 1.0             │
        │ 21    ┆ 2001-01-01 21:00:00 ┆ 1.0             │
        │ 22    ┆ 2001-01-01 22:00:00 ┆ 1.0             │
        │ 23    ┆ 2001-01-01 23:00:00 ┆ 1.0             │
        │ 24    ┆ 2001-01-02 00:00:00 ┆ 1.0             │
        └───────┴─────────────────────┴─────────────────┘
        """
        window_size = deprecate_saturating(window_size)
        window_size = _prepare_rolling_by_window_args(window_size)
        if warn_if_unsorted is not None:
            issue_deprecation_warning(
                "`warn_if_unsorted` is deprecated in `rolling_std_by` because it "
                "no longer requires sorted data - you can safely remove this argument.",
                version="0.20.27",
            )
        by = parse_as_expression(by)
        return self._from_pyexpr(
            self._pyexpr.rolling_std_by(
                by,
                window_size,
                min_periods,
                closed,
                ddof,
            )
        )
