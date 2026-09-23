    def _reduce(
        self, name: str, *, skipna: bool = True, keepdims: bool = False, **kwargs
    ):
        """
        Return a scalar result of performing the reduction operation.

        Parameters
        ----------
        name : str
            Name of the function, supported values are:
            { any, all, min, max, sum, mean, median, prod,
            std, var, sem, kurt, skew }.
        skipna : bool, default True
            If True, skip NaN values.
        **kwargs
            Additional keyword arguments passed to the reduction function.
            Currently, `ddof` is the only supported kwarg.

        Returns
        -------
        scalar

        Raises
        ------
        TypeError : subclass does not define reductions
        """
        pa_result = self._reduce_pyarrow(name, skipna=skipna, **kwargs)

        if keepdims:
            result = pa.array([pa_result.as_py()], type=pa_result.type)
            return type(self)(result)

        if pc.is_null(pa_result).as_py():
            return self.dtype.na_value
        else:
            return pa_result.as_py()
