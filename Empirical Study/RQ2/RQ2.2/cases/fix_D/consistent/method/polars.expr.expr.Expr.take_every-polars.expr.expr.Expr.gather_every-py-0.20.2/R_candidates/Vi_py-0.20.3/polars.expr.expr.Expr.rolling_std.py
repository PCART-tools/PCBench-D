    def rolling_std(
        self,
        window_size: int | timedelta | str,
        weights: list[float] | None = None,
        min_periods: int | None = None,
        *,
        center: bool = False,
        by: str | None = None,
        closed: ClosedInterval = "right",
        ddof: int = 1,
        warn_if_unsorted: bool = True,
    ) -> Self:
        """
        Compute a rolling standard deviation.

        If `by` has not been specified (the default), the window at a given row will
        include the row itself, and the `window_size - 1` elements before it.

        If you pass a `by` column `<t_0, t_1, ..., t_n>`, then `closed="left"` means
        the windows will be:

            - [t_0 - window_size, t_0)
            - [t_1 - window_size, t_1)
            - ...
            - [t_n - window_size, t_n)

        With `closed="right"`, the left endpoint is not included and the right
        endpoint is included.

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
            An optional slice with the same length as the window that determines the
            relative contribution of each value in a window to the output.
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
            be of dtype Datetime or Date.

            .. warning::
                If passed, the column must be sorted in ascending order. Otherwise,
                results will not be correct.
        closed : {'left', 'right', 'both', 'none'}
            Define which sides of the temporal interval are closed (inclusive); only
            applicable if `by` has been set.
        ddof
            "Delta Degrees of Freedom": The divisor for a length N window is N - ddof
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
        ...     rolling_std=pl.col("A").rolling_std(window_size=2),
        ... )
        shape: (6, 2)
        ┌─────┬─────────────┐
        │ A   ┆ rolling_std │
        │ --- ┆ ---         │
        │ f64 ┆ f64         │
        ╞═════╪═════════════╡
        │ 1.0 ┆ null        │
        │ 2.0 ┆ 0.707107    │
        │ 3.0 ┆ 0.707107    │
        │ 4.0 ┆ 0.707107    │
        │ 5.0 ┆ 0.707107    │
        │ 6.0 ┆ 0.707107    │
        └─────┴─────────────┘

        Specify weights to multiply the values in the window with:

        >>> df.with_columns(
        ...     rolling_std=pl.col("A").rolling_std(
        ...         window_size=2, weights=[0.25, 0.75]
        ...     ),
        ... )
        shape: (6, 2)
        ┌─────┬─────────────┐
        │ A   ┆ rolling_std │
        │ --- ┆ ---         │
        │ f64 ┆ f64         │
        ╞═════╪═════════════╡
        │ 1.0 ┆ null        │
        │ 2.0 ┆ 0.433013    │
        │ 3.0 ┆ 0.433013    │
        │ 4.0 ┆ 0.433013    │
        │ 5.0 ┆ 0.433013    │
        │ 6.0 ┆ 0.433013    │
        └─────┴─────────────┘

        Center the values in the window

        >>> df.with_columns(
        ...     rolling_std=pl.col("A").rolling_std(window_size=3, center=True),
        ... )
        shape: (6, 2)
        ┌─────┬─────────────┐
        │ A   ┆ rolling_std │
        │ --- ┆ ---         │
        │ f64 ┆ f64         │
        ╞═════╪═════════════╡
        │ 1.0 ┆ null        │
        │ 2.0 ┆ 1.0         │
        │ 3.0 ┆ 1.0         │
        │ 4.0 ┆ 1.0         │
        │ 5.0 ┆ 1.0         │
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

        Compute the rolling std with the default left closure of temporal windows

        >>> df_temporal.with_columns(
        ...     rolling_row_std=pl.col("row_nr").rolling_std(
        ...         window_size="2h", by="date", closed="left"
        ...     )
        ... )
        shape: (25, 3)
        ┌────────┬─────────────────────┬─────────────────┐
        │ row_nr ┆ date                ┆ rolling_row_std │
        │ ---    ┆ ---                 ┆ ---             │
        │ u32    ┆ datetime[μs]        ┆ f64             │
        ╞════════╪═════════════════════╪═════════════════╡
        │ 0      ┆ 2001-01-01 00:00:00 ┆ null            │
        │ 1      ┆ 2001-01-01 01:00:00 ┆ 0.0             │
        │ 2      ┆ 2001-01-01 02:00:00 ┆ 0.707107        │
        │ 3      ┆ 2001-01-01 03:00:00 ┆ 0.707107        │
        │ …      ┆ …                   ┆ …               │
        │ 21     ┆ 2001-01-01 21:00:00 ┆ 0.707107        │
        │ 22     ┆ 2001-01-01 22:00:00 ┆ 0.707107        │
        │ 23     ┆ 2001-01-01 23:00:00 ┆ 0.707107        │
        │ 24     ┆ 2001-01-02 00:00:00 ┆ 0.707107        │
        └────────┴─────────────────────┴─────────────────┘

        Compute the rolling std with the closure of windows on both sides

        >>> df_temporal.with_columns(
        ...     rolling_row_std=pl.col("row_nr").rolling_std(
        ...         window_size="2h", by="date", closed="both"
        ...     )
        ... )
        shape: (25, 3)
        ┌────────┬─────────────────────┬─────────────────┐
        │ row_nr ┆ date                ┆ rolling_row_std │
        │ ---    ┆ ---                 ┆ ---             │
        │ u32    ┆ datetime[μs]        ┆ f64             │
        ╞════════╪═════════════════════╪═════════════════╡
        │ 0      ┆ 2001-01-01 00:00:00 ┆ 0.0             │
        │ 1      ┆ 2001-01-01 01:00:00 ┆ 0.707107        │
        │ 2      ┆ 2001-01-01 02:00:00 ┆ 1.0             │
        │ 3      ┆ 2001-01-01 03:00:00 ┆ 1.0             │
        │ …      ┆ …                   ┆ …               │
        │ 21     ┆ 2001-01-01 21:00:00 ┆ 1.0             │
        │ 22     ┆ 2001-01-01 22:00:00 ┆ 1.0             │
        │ 23     ┆ 2001-01-01 23:00:00 ┆ 1.0             │
        │ 24     ┆ 2001-01-02 00:00:00 ┆ 1.0             │
        └────────┴─────────────────────┴─────────────────┘

        """
        window_size = deprecate_saturating(window_size)
        window_size, min_periods = _prepare_rolling_window_args(
            window_size, min_periods
        )
        return self._from_pyexpr(
            self._pyexpr.rolling_std(
                window_size,
                weights,
                min_periods,
                center,
                by,
                closed,
                ddof,
                warn_if_unsorted,
            )
        )
