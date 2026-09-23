    def max(
        self,
        numeric_only: bool = False,
        min_count: int = 0,
        *args,
        **kwargs,
    ):
        """
        Compute max value of group.

        Returns
        -------
        Series or DataFrame

        Examples
        --------
        >>> ser = pd.Series([1, 2, 3, 4], index=pd.DatetimeIndex(
        ...                 ['2023-01-01', '2023-01-15', '2023-02-01', '2023-02-15']))
        >>> ser
        2023-01-01    1
        2023-01-15    2
        2023-02-01    3
        2023-02-15    4
        dtype: int64
        >>> ser.resample('MS').max()
        2023-01-01    2
        2023-02-01    4
        Freq: MS, dtype: int64
        """
        maybe_warn_args_and_kwargs(type(self), "max", args, kwargs)
        nv.validate_resampler_func("max", args, kwargs)
        return self._downsample("max", numeric_only=numeric_only, min_count=min_count)
