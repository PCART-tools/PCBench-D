    def _apply(
        self,
        func: Callable,
        center: bool,
        require_min_periods: int = 0,
        floor: int = 1,
        is_weighted: bool = False,
        name: Optional[str] = None,
        use_numba_cache: bool = False,
        **kwargs,
    ):
        """
        Rolling statistical measure using supplied function.

        Designed to be used with passed-in Cython array-based functions.

        Parameters
        ----------
        func : callable function to apply
        center : bool
        require_min_periods : int
        floor : int
        is_weighted : bool
        name : str,
            compatibility with groupby.rolling
        use_numba_cache : bool
            whether to cache a numba compiled function. Only available for numba
            enabled methods (so far only apply)
        **kwargs
            additional arguments for rolling function and window function

        Returns
        -------
        y : type of input
        """
        win_type = self._get_win_type(kwargs)
        window = self._get_window(win_type=win_type)

        blocks, obj = self._create_blocks()
        block_list = list(blocks)
        window_indexer = self._get_window_indexer(window)

        results = []
        exclude: List[Scalar] = []
        for i, b in enumerate(blocks):
            try:
                values = self._prep_values(b.values)

            except (TypeError, NotImplementedError):
                if isinstance(obj, ABCDataFrame):
                    exclude.extend(b.columns)
                    del block_list[i]
                    continue
                else:
                    raise DataError("No numeric types to aggregate")

            if values.size == 0:
                results.append(values.copy())
                continue

            # calculation function
            offset = calculate_center_offset(window) if center else 0
            additional_nans = np.array([np.nan] * offset)

            if not is_weighted:

                def calc(x):
                    x = np.concatenate((x, additional_nans))
                    if not isinstance(window, BaseIndexer):
                        min_periods = calculate_min_periods(
                            window, self.min_periods, len(x), require_min_periods, floor
                        )
                    else:
                        min_periods = calculate_min_periods(
                            self.min_periods or 1,
                            self.min_periods,
                            len(x),
                            require_min_periods,
                            floor,
                        )
                    start, end = window_indexer.get_window_bounds(
                        num_values=len(x),
                        min_periods=self.min_periods,
                        center=self.center,
                        closed=self.closed,
                    )
                    return func(x, start, end, min_periods)

            else:

                def calc(x):
                    x = np.concatenate((x, additional_nans))
                    return func(x, window, self.min_periods)

            with np.errstate(all="ignore"):
                if values.ndim > 1:
                    result = np.apply_along_axis(calc, self.axis, values)
                else:
                    result = calc(values)
                    result = np.asarray(result)

            if use_numba_cache:
                self._numba_func_cache[name] = func

            if center:
                result = self._center_window(result, window)

            results.append(result)

        return self._wrap_results(results, block_list, obj, exclude)
