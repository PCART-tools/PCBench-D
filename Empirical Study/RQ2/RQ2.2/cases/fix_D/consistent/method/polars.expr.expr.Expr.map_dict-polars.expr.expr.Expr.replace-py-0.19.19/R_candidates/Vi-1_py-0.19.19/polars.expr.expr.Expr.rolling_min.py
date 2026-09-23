    @warn_closed_future_change()
    def rolling_min(
        self,
        window_size: int | timedelta | str,
        weights: list[float] | None = None,
        min_periods: int | None = None,
        *,
        center: bool = False,
        by: str | None = None,
        closed: ClosedInterval = "left",
        warn_if_unsorted: bool = True,
    ) -> Self:
        """
        Apply a rolling min (moving min) over the values in this array.

        A window of length `window_size` will traverse the array. The values that fill
        this window will (optionally) be multiplied with the weights given by the
        `weight` vector. The resulting values will be aggregated to their min.

        If `by` has not been specified (the default), the window at a given row will
        include the row itself, and the `window_size - 1` elements before it.

        If you pass a `by` column `<t_0, t_1, ..., t_n>`, then `closed="left"`
        means the windows will be:

            - [t_0 - window_size, t_0)
            - [t_1 - window_size, t_1)
            - ...
            - [t_n - window_size, t_n)

        With `closed="right"`, the left endpoint is not included and the right
        endpoint is included.

        Parameters
        ----------
        window_size
            The length of the window. Can be a fixed integer size, or a dynamic
            temporal size indicated by a timedelta or the following string language:

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
            a result. If None, it will be set equal to window size.
        center
            Set the labels at the center of the window
        by
            If the `window_size` is temporal for instance `"5h"` or `"3s"`, you must
            set the column that will be used to determine the windows. This column must
            be of dtype Datetime or Date.

            .. warning::
                If passed, the column must be sorted in ascending order. Otherwise,
                results will not be correct.
        closed : {'left', 'right', 'both', 'none'}
            Define which sides of the temporal interval are closed (inclusive); only
            applicable if `by` has been set.
        warn_if_unsorted
            Warn if data is not known to be sorted by `by` column (if passed).
            Experimental.

        Warnings
        --------
        This functionality is experimental and may change without it being considered a
        breaking change.

        Notes
        -----
        If you want to compute multiple aggregation statistics over the same dynamic
        window, consider using `rolling` - this method can cache the window size
        computation.

        Examples
        --------
        >>> df = pl.DataFrame({"A": [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]})
        >>> df.with_columns(
        ...     rolling_min=pl.col("A").rolling_min(window_size=2),
        ... )
        shape: (6, 2)
        ┌─────┬─────────────┐
        │ A   ┆ rolling_min │
        │ --- ┆ ---         │
        │ f64 ┆ f64         │
        ╞═════╪═════════════╡
        │ 1.0 ┆ null        │
        │ 2.0 ┆ 1.0         │
        │ 3.0 ┆ 2.0         │
        │ 4.0 ┆ 3.0         │
        │ 5.0 ┆ 4.0         │
        │ 6.0 ┆ 5.0         │
        └─────┴─────────────┘

        Specify weights to multiply the values in the window with:

        >>> df.with_columns(
        ...     rolling_min=pl.col("A").rolling_min(
        ...         window_size=2, weights=[0.25, 0.75]
        ...     ),
        ... )
        shape: (6, 2)
        ┌─────┬─────────────┐
        │ A   ┆ rolling_min │
        │ --- ┆ ---         │
        │ f64 ┆ f64         │
        ╞═════╪═════════════╡
        │ 1.0 ┆ null        │
        │ 2.0 ┆ 0.25        │
        │ 3.0 ┆ 0.5         │
        │ 4.0 ┆ 0.75        │
        │ 5.0 ┆ 1.0         │
        │ 6.0 ┆ 1.25        │
        └─────┴─────────────┘

        Center the values in the window

        >>> df.with_columns(
        ...     rolling_min=pl.col("A").rolling_min(window_size=3, center=True),
        ... )
        shape: (6, 2)
        ┌─────┬─────────────┐
        │ A   ┆ rolling_min │
        │ --- ┆ ---         │
        │ f64 ┆ f64         │
        ╞═════╪═════════════╡
        │ 1.0 ┆ null        │
        │ 2.0 ┆ 1.0         │
        │ 3.0 ┆ 2.0         │
        │ 4.0 ┆ 3.0         │
        │ 5.0 ┆ 4.0         │
        │ 6.0 ┆ null        │
        └─────┴─────────────┘

        Create a DataFrame with a datetime column and a row number column

        >>> from datetime import timedelta, datetime
        >>> start = datetime(2001, 1, 1)
        >>> stop = datetime(2001, 1, 2)
        >>> df_temporal = pl.DataFrame(
        ...     {"date": pl.datetime_range(start, stop, "1h", eager=True)}
        ... ).with_row_count()
        >>> df_temporal
        shape: (25, 2)
        ┌────────┬─────────────────────┐
        │ row_nr ┆ date                │
        │ ---    ┆ ---                 │
        │ u32    ┆ datetime[μs]        │
        ╞════════╪═════════════════════╡
        │ 0      ┆ 2001-01-01 00:00:00 │
        │ 1      ┆ 2001-01-01 01:00:00 │
        │ 2      ┆ 2001-01-01 02:00:00 │
        │ 3      ┆ 2001-01-01 03:00:00 │
        │ …      ┆ …                   │
        │ 21     ┆ 2001-01-01 21:00:00 │
        │ 22     ┆ 2001-01-01 22:00:00 │
        │ 23     ┆ 2001-01-01 23:00:00 │
        │ 24     ┆ 2001-01-02 00:00:00 │
        └────────┴─────────────────────┘
        >>> df_temporal.with_columns(
        ...     rolling_row_min=pl.col("row_nr").rolling_min(
        ...         window_size="2h", by="date", closed="left"
        ...     )
        ... )
        shape: (25, 3)
        ┌────────┬─────────────────────┬─────────────────┐
        │ row_nr ┆ date                ┆ rolling_row_min │
        │ ---    ┆ ---                 ┆ ---             │
        │ u32    ┆ datetime[μs]        ┆ u32             │
        ╞════════╪═════════════════════╪═════════════════╡
        │ 0      ┆ 2001-01-01 00:00:00 ┆ null            │
        │ 1      ┆ 2001-01-01 01:00:00 ┆ 0               │
        │ 2      ┆ 2001-01-01 02:00:00 ┆ 0               │
        │ 3      ┆ 2001-01-01 03:00:00 ┆ 1               │
        │ …      ┆ …                   ┆ …               │
        │ 21     ┆ 2001-01-01 21:00:00 ┆ 19              │
        │ 22     ┆ 2001-01-01 22:00:00 ┆ 20              │
        │ 23     ┆ 2001-01-01 23:00:00 ┆ 21              │
        │ 24     ┆ 2001-01-02 00:00:00 ┆ 22              │
        └────────┴─────────────────────┴─────────────────┘

        """
        window_size = deprecate_saturating(window_size)
        window_size, min_periods = _prepare_rolling_window_args(
            window_size, min_periods
        )
        return self._from_pyexpr(
            self._pyexpr.rolling_min(
                window_size, weights, min_periods, center, by, closed, warn_if_unsorted
            )
        )
