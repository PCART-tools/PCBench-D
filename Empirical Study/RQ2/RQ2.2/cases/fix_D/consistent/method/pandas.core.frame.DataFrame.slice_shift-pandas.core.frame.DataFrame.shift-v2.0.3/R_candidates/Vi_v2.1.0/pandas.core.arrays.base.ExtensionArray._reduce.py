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
        keepdims : bool, default False
            If False, a scalar is returned.
            If True, the result has dimension with size one along the reduced axis.

            .. versionadded:: 2.1

               This parameter is not required in the _reduce signature to keep backward
               compatibility, but will become required in the future. If the parameter
               is not found in the method signature, a FutureWarning will be emitted.
        **kwargs
            Additional keyword arguments passed to the reduction function.
            Currently, `ddof` is the only supported kwarg.

        Returns
        -------
        scalar

        Raises
        ------
        TypeError : subclass does not define reductions

        Examples
        --------
        >>> pd.array([1, 2, 3])._reduce("min")
        1
        """
        meth = getattr(self, name, None)
        if meth is None:
            raise TypeError(
                f"'{type(self).__name__}' with dtype {self.dtype} "
                f"does not support reduction '{name}'"
            )
        result = meth(skipna=skipna, **kwargs)
        if keepdims:
            result = np.array([result])

        return result
