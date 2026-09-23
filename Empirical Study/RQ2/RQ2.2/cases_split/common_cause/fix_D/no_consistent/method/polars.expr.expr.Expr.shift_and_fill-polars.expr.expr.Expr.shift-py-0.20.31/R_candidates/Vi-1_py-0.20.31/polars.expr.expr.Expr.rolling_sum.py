    @unstable()
    def rolling_sum(
        self,
        window_size: int | timedelta | str,
        weights: list[float] | None = None,
        min_periods: int | None = None,
        *,
        center: bool = False,
        by: str | None = None,
        closed: ClosedInterval | None = None,
        warn_if_unsorted: bool | None = None,
    ) -> Self:
        """
        Apply a rolling sum (moving sum) over the values in this array.

        .. warning::
            This functionality is considered **unstable**. It may be changed
            at any point without it being considered a breaking change.

        A window of length `window_size` will traverse the array. The values that fill
        this window will (optionally) be multiplied with the weights given by the
        `weight` vector. The resulting values will be aggregated to their sum.

        If `by` has not been specified (the default), the window at a given row will
        include the row itself, and the `window_size - 1` elements before it.

        If you pass a `by` column `<t_0, t_1, ..., t_n>`, then `closed="right"`
        (the default) means the windows will be:

            - (t_0 - window_size, t_0]
            - (t_1 - window_size, t_1]
            - ...
            - (t_n - window_size, t_n]

        Parameters
        ----------
        window_size
            The length of the window. Can be a fixed integer size, or a dynamic temporal
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
            - 1i    (1 index count)

            By "calendar day", we mean the corresponding time on the next day
            (which may not be 24 hours, due to daylight savings). Similarly for
            "calendar week", "calendar month", "calendar quarter", and
            "calendar year".

            If a timedelta or the dynamic string language is used, the `by`
            and `closed` arguments must also be set.
        weights
            An optional slice with the same length as the window that will be multiplied
            elementwise with the values in the window.
        min_periods
            The number of values in the window that should be non-null before computing
            a result. If None, it will be set equal to:

            - the window size, if `window_size` is a fixed integer
            - 1, if `window_size` is a dynamic temporal size
        center
            Set the labels at the center of the window
        by
            If the `window_size` is temporal for instance `"5h"` or `"3s"`, you must
            set the column that will be used to determine the windows. This column must
            of dtype `{Date, Datetime}`

            .. deprecated:: 0.20.24
                Passing `by` to `rolling_sum` is deprecated - please use
                :meth:`.rolling_sum_by` instead.
        closed : {'left', 'right', 'both', 'none'}
            Define which sides of the temporal interval are closed (inclusive); only
            applicable if `by` has been set (in which case, it defaults to `'right'`).
        warn_if_unsorted
            Warn if data is not known to be sorted by `by` column (if passed).

        Notes
        -----
        If you want to compute multiple aggregation statistics over the same dynamic
        window, consider using `rolling` - this method can cache the window size
        computation.

        Examples
        --------
        >>> df = pl.DataFrame({"A": [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]})
        >>> df.with_columns(
        ...     rolling_sum=pl.col("A").rolling_sum(window_size=2),
        ... )
        shape: (6, 2)
        ┌─────┬─────────────┐
        │ A   ┆ rolling_sum │
        │ --- ┆ ---         │
        │ f64 ┆ f64         │
        ╞═════╪═════════════╡
        │ 1.0 ┆ null        │
        │ 2.0 ┆ 3.0         │
        │ 3.0 ┆ 5.0         │
        │ 4.0 ┆ 7.0         │
        │ 5.0 ┆ 9.0         │
        │ 6.0 ┆ 11.0        │
        └─────┴─────────────┘

        Specify weights to multiply the values in the window with:

        >>> df.with_columns(
        ...     rolling_sum=pl.col("A").rolling_sum(
        ...         window_size=2, weights=[0.25, 0.75]
        ...     ),
        ... )
        shape: (6, 2)
        ┌─────┬─────────────┐
        │ A   ┆ rolling_sum │
        │ --- ┆ ---         │
        │ f64 ┆ f64         │
        ╞═════╪═════════════╡
        │ 1.0 ┆ null        │
        │ 2.0 ┆ 1.75        │
        │ 3.0 ┆ 2.75        │
        │ 4.0 ┆ 3.75        │
        │ 5.0 ┆ 4.75        │
        │ 6.0 ┆ 5.75        │
        └─────┴─────────────┘

        Center the values in the window

        >>> df.with_columns(
        ...     rolling_sum=pl.col("A").rolling_sum(window_size=3, center=True),
        ... )
        shape: (6, 2)
        ┌─────┬─────────────┐
        │ A   ┆ rolling_sum │
        │ --- ┆ ---         │
        │ f64 ┆ f64         │
        ╞═════╪═════════════╡
        │ 1.0 ┆ null        │
        │ 2.0 ┆ 6.0         │
        │ 3.0 ┆ 9.0         │
        │ 4.0 ┆ 12.0        │
        │ 5.0 ┆ 15.0        │
        │ 6.0 ┆ null        │
        └─────┴─────────────┘

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

        Compute the rolling sum with the temporal windows closed on the right (default)

        >>> df_temporal.with_columns(
        ...     rolling_row_sum=pl.col("index").rolling_sum(window_size="2h", by="date")
        ... )  # doctest:+SKIP
        shape: (25, 3)
        ┌───────┬─────────────────────┬─────────────────┐
        │ index ┆ date                ┆ rolling_row_sum │
        │ ---   ┆ ---                 ┆ ---             │
        │ u32   ┆ datetime[μs]        ┆ u32             │
        ╞═══════╪═════════════════════╪═════════════════╡
        │ 0     ┆ 2001-01-01 00:00:00 ┆ 0               │
        │ 1     ┆ 2001-01-01 01:00:00 ┆ 1               │
        │ 2     ┆ 2001-01-01 02:00:00 ┆ 3               │
        │ 3     ┆ 2001-01-01 03:00:00 ┆ 5               │
        │ 4     ┆ 2001-01-01 04:00:00 ┆ 7               │
        │ …     ┆ …                   ┆ …               │
        │ 20    ┆ 2001-01-01 20:00:00 ┆ 39              │
        │ 21    ┆ 2001-01-01 21:00:00 ┆ 41              │
        │ 22    ┆ 2001-01-01 22:00:00 ┆ 43              │
        │ 23    ┆ 2001-01-01 23:00:00 ┆ 45              │
        │ 24    ┆ 2001-01-02 00:00:00 ┆ 47              │
        └───────┴─────────────────────┴─────────────────┘

        Compute the rolling sum with the closure of windows on both sides

        >>> df_temporal.with_columns(
        ...     rolling_row_sum=pl.col("index").rolling_sum(
        ...         window_size="2h", by="date", closed="both"
        ...     )
        ... )  # doctest:+SKIP
        shape: (25, 3)
        ┌───────┬─────────────────────┬─────────────────┐
        │ index ┆ date                ┆ rolling_row_sum │
        │ ---   ┆ ---                 ┆ ---             │
        │ u32   ┆ datetime[μs]        ┆ u32             │
        ╞═══════╪═════════════════════╪═════════════════╡
        │ 0     ┆ 2001-01-01 00:00:00 ┆ 0               │
        │ 1     ┆ 2001-01-01 01:00:00 ┆ 1               │
        │ 2     ┆ 2001-01-01 02:00:00 ┆ 3               │
        │ 3     ┆ 2001-01-01 03:00:00 ┆ 6               │
        │ 4     ┆ 2001-01-01 04:00:00 ┆ 9               │
        │ …     ┆ …                   ┆ …               │
        │ 20    ┆ 2001-01-01 20:00:00 ┆ 57              │
        │ 21    ┆ 2001-01-01 21:00:00 ┆ 60              │
        │ 22    ┆ 2001-01-01 22:00:00 ┆ 63              │
        │ 23    ┆ 2001-01-01 23:00:00 ┆ 66              │
        │ 24    ┆ 2001-01-02 00:00:00 ┆ 69              │
        └───────┴─────────────────────┴─────────────────┘
        """
        window_size = deprecate_saturating(window_size)
        window_size, min_periods = _prepare_rolling_window_args(
            window_size, min_periods
        )
        if by is not None:
            issue_deprecation_warning(
                "Passing `by` to `rolling_sum` is deprecated. Instead of "
                "`rolling_sum(..., by='foo')`, please use `rolling_sum_by('foo', ...)`.",
                version="0.20.24",
            )
            validate_rolling_by_aggs_arguments(weights, center=center)
            return self.rolling_sum_by(
                by=by,
                # integer `window_size` was already not supported when `by` was passed
                window_size=window_size,  # type: ignore[arg-type]
                min_periods=min_periods,
                closed=closed or "right",
                warn_if_unsorted=warn_if_unsorted,
            )
        window_size = validate_rolling_aggs_arguments(window_size, closed)
        return self._from_pyexpr(
            self._pyexpr.rolling_sum(
                window_size,
                weights,
                min_periods,
                center,
            )
        )
