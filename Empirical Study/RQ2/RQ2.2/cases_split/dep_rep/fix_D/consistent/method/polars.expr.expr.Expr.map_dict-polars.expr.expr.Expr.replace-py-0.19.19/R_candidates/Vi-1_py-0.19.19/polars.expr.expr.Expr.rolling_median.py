    @warn_closed_future_change()
    def rolling_median(
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
        Compute a rolling median.

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
        ...     rolling_median=pl.col("A").rolling_median(window_size=2),
        ... )
        shape: (6, 2)
        ┌─────┬────────────────┐
        │ A   ┆ rolling_median │
        │ --- ┆ ---            │
        │ f64 ┆ f64            │
        ╞═════╪════════════════╡
        │ 1.0 ┆ null           │
        │ 2.0 ┆ 1.5            │
        │ 3.0 ┆ 2.5            │
        │ 4.0 ┆ 3.5            │
        │ 5.0 ┆ 4.5            │
        │ 6.0 ┆ 5.5            │
        └─────┴────────────────┘

        Specify weights for the values in each window:

        >>> df.with_columns(
        ...     rolling_median=pl.col("A").rolling_median(
        ...         window_size=2, weights=[0.25, 0.75]
        ...     ),
        ... )
        shape: (6, 2)
        ┌─────┬────────────────┐
        │ A   ┆ rolling_median │
        │ --- ┆ ---            │
        │ f64 ┆ f64            │
        ╞═════╪════════════════╡
        │ 1.0 ┆ null           │
        │ 2.0 ┆ 1.5            │
        │ 3.0 ┆ 2.5            │
        │ 4.0 ┆ 3.5            │
        │ 5.0 ┆ 4.5            │
        │ 6.0 ┆ 5.5            │
        └─────┴────────────────┘

        Center the values in the window

        >>> df.with_columns(
        ...     rolling_median=pl.col("A").rolling_median(window_size=3, center=True),
        ... )
        shape: (6, 2)
        ┌─────┬────────────────┐
        │ A   ┆ rolling_median │
        │ --- ┆ ---            │
        │ f64 ┆ f64            │
        ╞═════╪════════════════╡
        │ 1.0 ┆ null           │
        │ 2.0 ┆ 2.0            │
        │ 3.0 ┆ 3.0            │
        │ 4.0 ┆ 4.0            │
        │ 5.0 ┆ 5.0            │
        │ 6.0 ┆ null           │
        └─────┴────────────────┘

        """
        window_size = deprecate_saturating(window_size)
        window_size, min_periods = _prepare_rolling_window_args(
            window_size, min_periods
        )
        return self._from_pyexpr(
            self._pyexpr.rolling_median(
                window_size, weights, min_periods, center, by, closed, warn_if_unsorted
            )
        )
