    @unstable()
    def rolling_var(
        self,
        window_size: int | timedelta,
        weights: list[float] | None = None,
        *,
        min_periods: int | None = None,
        center: bool = False,
        ddof: int = 1,
    ) -> Expr:
        """
        Compute a rolling variance.

        .. warning::
            This functionality is considered **unstable**. It may be changed
            at any point without it being considered a breaking change.

        A window of length `window_size` will traverse the array. The values that fill
        this window will (optionally) be multiplied with the weights given by the
        `weights` vector. The resulting values will be aggregated to their var.

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
        ddof
            "Delta Degrees of Freedom": The divisor for a length N window is N - ddof

        Notes
        -----
        If you want to compute multiple aggregation statistics over the same dynamic
        window, consider using `rolling` - this method can cache the window size
        computation.

        Examples
        --------
        >>> df = pl.DataFrame({"A": [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]})
        >>> df.with_columns(
        ...     rolling_var=pl.col("A").rolling_var(window_size=2),
        ... )
        shape: (6, 2)
        ┌─────┬─────────────┐
        │ A   ┆ rolling_var │
        │ --- ┆ ---         │
        │ f64 ┆ f64         │
        ╞═════╪═════════════╡
        │ 1.0 ┆ null        │
        │ 2.0 ┆ 0.5         │
        │ 3.0 ┆ 0.5         │
        │ 4.0 ┆ 0.5         │
        │ 5.0 ┆ 0.5         │
        │ 6.0 ┆ 0.5         │
        └─────┴─────────────┘

        Specify weights to multiply the values in the window with:

        >>> df.with_columns(
        ...     rolling_var=pl.col("A").rolling_var(
        ...         window_size=2, weights=[0.25, 0.75]
        ...     ),
        ... )
        shape: (6, 2)
        ┌─────┬─────────────┐
        │ A   ┆ rolling_var │
        │ --- ┆ ---         │
        │ f64 ┆ f64         │
        ╞═════╪═════════════╡
        │ 1.0 ┆ null        │
        │ 2.0 ┆ 0.1875      │
        │ 3.0 ┆ 0.1875      │
        │ 4.0 ┆ 0.1875      │
        │ 5.0 ┆ 0.1875      │
        │ 6.0 ┆ 0.1875      │
        └─────┴─────────────┘

        Center the values in the window

        >>> df.with_columns(
        ...     rolling_var=pl.col("A").rolling_var(window_size=3, center=True),
        ... )
        shape: (6, 2)
        ┌─────┬─────────────┐
        │ A   ┆ rolling_var │
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
        """
        return self._from_pyexpr(
            self._pyexpr.rolling_var(
                window_size,
                weights,
                min_periods,
                center=center,
                ddof=ddof,
            )
        )
