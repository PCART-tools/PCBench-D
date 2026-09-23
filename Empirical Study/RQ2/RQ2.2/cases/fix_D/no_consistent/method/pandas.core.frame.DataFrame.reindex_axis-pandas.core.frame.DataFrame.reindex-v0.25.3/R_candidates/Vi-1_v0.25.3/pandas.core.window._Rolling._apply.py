    def _apply(
        self, func, name=None, window=None, center=None, check_minp=None, **kwargs
    ):
        """
        Rolling statistical measure using supplied function.

        Designed to be used with passed-in Cython array-based functions.

        Parameters
        ----------
        func : str/callable to apply
        name : str, optional
           name of this function
        window : int/array, default to _get_window()
        center : bool, default to self.center
        check_minp : function, default to _use_window

        Returns
        -------
        y : type of input
        """
        if center is None:
            center = self.center
        if window is None:
            window = self._get_window()

        if check_minp is None:
            check_minp = _use_window

        blocks, obj = self._create_blocks()
        block_list = list(blocks)
        index_as_array = self._get_index()

        results = []
        exclude = []
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

            # if we have a string function name, wrap it
            if isinstance(func, str):
                cfunc = getattr(libwindow, func, None)
                if cfunc is None:
                    raise ValueError(
                        "we do not support this function "
                        "in libwindow.{func}".format(func=func)
                    )

                def func(arg, window, min_periods=None, closed=None):
                    minp = check_minp(min_periods, window)
                    # ensure we are only rolling on floats
                    arg = ensure_float64(arg)
                    return cfunc(arg, window, minp, index_as_array, closed, **kwargs)

            # calculation function
            if center:
                offset = _offset(window, center)
                additional_nans = np.array([np.NaN] * offset)

                def calc(x):
                    return func(
                        np.concatenate((x, additional_nans)),
                        window,
                        min_periods=self.min_periods,
                        closed=self.closed,
                    )

            else:

                def calc(x):
                    return func(
                        x, window, min_periods=self.min_periods, closed=self.closed
                    )

            with np.errstate(all="ignore"):
                if values.ndim > 1:
                    result = np.apply_along_axis(calc, self.axis, values)
                else:
                    result = calc(values)

            if center:
                result = self._center_window(result, window)

            results.append(result)

        return self._wrap_results(results, block_list, obj, exclude)
