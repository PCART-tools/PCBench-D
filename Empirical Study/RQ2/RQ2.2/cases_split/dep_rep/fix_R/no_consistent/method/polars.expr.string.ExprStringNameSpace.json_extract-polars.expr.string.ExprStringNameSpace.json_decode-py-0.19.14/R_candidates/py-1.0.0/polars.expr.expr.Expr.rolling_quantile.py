    @unstable()
    def rolling_quantile(
        self,
        quantile: float,
        interpolation: RollingInterpolationMethod = "nearest",
        window_size: int | timedelta = 2,
        weights: list[float] | None = None,
        *,
        min_periods: int | None = None,
        center: bool = False,
    ) -> Expr:
        """
        Compute a rolling quantile.

        .. warning::
            This functionality is considered **unstable**. It may be changed
            at any point without it being considered a breaking change.

        A window of length `window_size` will traverse the array. The values that fill
        this window will (optionally) be multiplied with the weights given by the
        `weights` vector. The resulting values will be aggregated to their quantile.

        The window at a given row will include the row itself, and the `window_size - 1`
        elements before it.

        Parameters
        ----------
        quantile
            Quantile between 0.0 and 1.0.
        interpolation : {'nearest', 'higher', 'lower', 'midpoint', 'linear'}
            Interpolation method.
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
        ...     rolling_quantile=pl.col("A").rolling_quantile(
        ...         quantile=0.25, window_size=4
        ...     ),
        ... )
        shape: (6, 2)
        ┌─────┬──────────────────┐
        │ A   ┆ rolling_quantile │
        │ --- ┆ ---              │
        │ f64 ┆ f64              │
        ╞═════╪══════════════════╡
        │ 1.0 ┆ null             │
        │ 2.0 ┆ null             │
        │ 3.0 ┆ null             │
        │ 4.0 ┆ 2.0              │
        │ 5.0 ┆ 3.0              │
        │ 6.0 ┆ 4.0              │
        └─────┴──────────────────┘

        Specify weights for the values in each window:

        >>> df.with_columns(
        ...     rolling_quantile=pl.col("A").rolling_quantile(
        ...         quantile=0.25, window_size=4, weights=[0.2, 0.4, 0.4, 0.2]
        ...     ),
        ... )
        shape: (6, 2)
        ┌─────┬──────────────────┐
        │ A   ┆ rolling_quantile │
        │ --- ┆ ---              │
        │ f64 ┆ f64              │
        ╞═════╪══════════════════╡
        │ 1.0 ┆ null             │
        │ 2.0 ┆ null             │
        │ 3.0 ┆ null             │
        │ 4.0 ┆ 2.0              │
        │ 5.0 ┆ 3.0              │
        │ 6.0 ┆ 4.0              │
        └─────┴──────────────────┘

        Specify weights and interpolation method

        >>> df.with_columns(
        ...     rolling_quantile=pl.col("A").rolling_quantile(
        ...         quantile=0.25,
        ...         window_size=4,
        ...         weights=[0.2, 0.4, 0.4, 0.2],
        ...         interpolation="linear",
        ...     ),
        ... )
        shape: (6, 2)
        ┌─────┬──────────────────┐
        │ A   ┆ rolling_quantile │
        │ --- ┆ ---              │
        │ f64 ┆ f64              │
        ╞═════╪══════════════════╡
        │ 1.0 ┆ null             │
        │ 2.0 ┆ null             │
        │ 3.0 ┆ null             │
        │ 4.0 ┆ 1.625            │
        │ 5.0 ┆ 2.625            │
        │ 6.0 ┆ 3.625            │
        └─────┴──────────────────┘

        Center the values in the window

        >>> df.with_columns(
        ...     rolling_quantile=pl.col("A").rolling_quantile(
        ...         quantile=0.2, window_size=5, center=True
        ...     ),
        ... )
        shape: (6, 2)
        ┌─────┬──────────────────┐
        │ A   ┆ rolling_quantile │
        │ --- ┆ ---              │
        │ f64 ┆ f64              │
        ╞═════╪══════════════════╡
        │ 1.0 ┆ null             │
        │ 2.0 ┆ null             │
        │ 3.0 ┆ 2.0              │
        │ 4.0 ┆ 3.0              │
        │ 5.0 ┆ null             │
        │ 6.0 ┆ null             │
        └─────┴──────────────────┘
        """
        return self._from_pyexpr(
            self._pyexpr.rolling_quantile(
                quantile,
                interpolation,
                window_size,
                weights,
                min_periods,
                center=center,
            )
        )
