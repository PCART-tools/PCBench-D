    @unstable()
    def rolling_map(
        self,
        function: Callable[[Series], Any],
        window_size: int,
        weights: list[float] | None = None,
        *,
        min_periods: int | None = None,
        center: bool = False,
    ) -> Series:
        """
        Compute a custom rolling window function.

        .. warning::
            This functionality is considered **unstable**. It may be changed
            at any point without it being considered a breaking change.

        Parameters
        ----------
        function
            Custom aggregation function.
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

        Warnings
        --------
        Computing custom functions is extremely slow. Use specialized rolling
        functions such as :func:`Series.rolling_sum` if at all possible.

        Examples
        --------
        >>> from numpy import nansum
        >>> s = pl.Series([11.0, 2.0, 9.0, float("nan"), 8.0])
        >>> s.rolling_map(nansum, window_size=3)
        shape: (5,)
        Series: '' [f64]
        [
                null
                null
                22.0
                11.0
                17.0
        ]
        """
