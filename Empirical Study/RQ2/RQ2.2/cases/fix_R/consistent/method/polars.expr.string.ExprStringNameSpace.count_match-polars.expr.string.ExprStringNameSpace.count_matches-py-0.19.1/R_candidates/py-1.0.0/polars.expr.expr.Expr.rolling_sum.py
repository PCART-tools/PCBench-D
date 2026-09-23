    @unstable()
    def rolling_sum(
        self,
        window_size: int | timedelta,
        weights: list[float] | None = None,
        *,
        min_periods: int | None = None,
        center: bool = False,
    ) -> Expr:
        """
        Apply a rolling sum (moving sum) over the values in this array.

        .. warning::
            This functionality is considered **unstable**. It may be changed
            at any point without it being considered a breaking change.

        A window of length `window_size` will traverse the array. The values that fill
        this window will (optionally) be multiplied with the weights given by the
        `weights` vector. The resulting values will be aggregated to their sum.

        The window at a given row will include the row itself, and the `window_size - 1`
        elements before it.

        Parameters
        ----------
        window_size
            The length of the window in number of elements.
        weights
            An optional slice with the same length as the window that will be multiplied
            elementwise with the values in the window.
        min_periods
            The number of values in the window that should be non-null before computing
            a result. If set to `None` (default), it will be set equal to `window_size`.
        center
            Set the labels at the center of the window.

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
        """
        return self._from_pyexpr(
            self._pyexpr.rolling_sum(
                window_size,
                weights,
                min_periods,
                center,
            )
        )
