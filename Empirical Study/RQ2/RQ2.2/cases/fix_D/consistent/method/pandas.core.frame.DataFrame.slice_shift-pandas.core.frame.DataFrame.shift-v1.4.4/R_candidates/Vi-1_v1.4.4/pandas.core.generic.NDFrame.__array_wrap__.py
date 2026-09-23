    def __array_wrap__(
        self,
        result: np.ndarray,
        context: tuple[Callable, tuple[Any, ...], int] | None = None,
    ):
        """
        Gets called after a ufunc and other functions.

        Parameters
        ----------
        result: np.ndarray
            The result of the ufunc or other function called on the NumPy array
            returned by __array__
        context: tuple of (func, tuple, int)
            This parameter is returned by ufuncs as a 3-element tuple: (name of the
            ufunc, arguments of the ufunc, domain of the ufunc), but is not set by
            other numpy functions.q

        Notes
        -----
        Series implements __array_ufunc_ so this not called for ufunc on Series.
        """
        # Note: at time of dask 2022.01.0, this is still used by dask
        res = lib.item_from_zerodim(result)
        if is_scalar(res):
            # e.g. we get here with np.ptp(series)
            # ptp also requires the item_from_zerodim
            return res
        d = self._construct_axes_dict(self._AXIS_ORDERS, copy=False)
        return self._constructor(res, **d).__finalize__(self, method="__array_wrap__")
