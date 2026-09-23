    def _apply(
        self,
        func: Callable[..., Any],
        name: str | None = None,
        numba_cache_key: tuple[Callable, str] | None = None,
        numba_args: tuple[Any, ...] = (),
        **kwargs,
    ):
        """
        Rolling statistical measure using supplied function.

        Designed to be used with passed-in Cython array-based functions.

        Parameters
        ----------
        func : callable function to apply
        name : str,
        numba_cache_key : tuple
            caching key to be used to store a compiled numba func
        numba_args : tuple
            args to be passed when func is a numba func
        **kwargs
            additional arguments for rolling function and window function

        Returns
        -------
        y : type of input
        """
        window_indexer = self._get_window_indexer()
        min_periods = (
            self.min_periods
            if self.min_periods is not None
            else window_indexer.window_size
        )

        def homogeneous_func(values: np.ndarray):
            # calculation function

            if values.size == 0:
                return values.copy()

            def calc(x):
                start, end = window_indexer.get_window_bounds(
                    num_values=len(x),
                    min_periods=min_periods,
                    center=self.center,
                    closed=self.closed,
                )
                self._check_window_bounds(start, end, len(x))

                return func(x, start, end, min_periods, *numba_args)

            with np.errstate(all="ignore"):
                result = calc(values)

            if numba_cache_key is not None:
                NUMBA_FUNC_CACHE[numba_cache_key] = func

            return result

        if self.method == "single":
            return self._apply_blockwise(homogeneous_func, name)
        else:
            return self._apply_tablewise(homogeneous_func, name)
