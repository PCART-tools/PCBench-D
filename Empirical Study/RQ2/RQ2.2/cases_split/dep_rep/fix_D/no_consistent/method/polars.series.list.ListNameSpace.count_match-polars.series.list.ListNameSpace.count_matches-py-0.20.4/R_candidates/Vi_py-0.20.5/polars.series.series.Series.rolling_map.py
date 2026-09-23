    def rolling_map(
        self,
        function: Callable[[Series], Any],
        window_size: int,
        weights: list[float] | None = None,
        min_periods: int | None = None,
        *,
        center: bool = False,
    ) -> Series:
        """
        Compute a custom rolling window function.

        .. warning::
            Computing custom functions is extremely slow. Use specialized rolling
            functions such as :func:`Series.rolling_sum` if at all possible.

        Parameters
        ----------
        function
            Custom aggregation function.
        window_size
            Size of the window. The window at a given row will include the row
            itself and the `window_size - 1` elements before it.
        weights
            A list of weights with the same length as the window that will be multiplied
            elementwise with the values in the window.
        min_periods
            The number of values in the window that should be non-null before computing
            a result. If None, it will be set equal to:

            - the window size, if `window_size` is a fixed integer
            - 1, if `window_size` is a dynamic temporal size
        center
            Set the labels at the center of the window.

        Warnings
        --------


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
