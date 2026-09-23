    @final
    def pct_change(
        self,
        periods: int = 1,
        fill_method: FillnaOptions | None | lib.NoDefault = lib.no_default,
        limit: int | None | lib.NoDefault = lib.no_default,
        freq=None,
        **kwargs,
    ) -> Self:
        """
        Fractional change between the current and a prior element.

        Computes the fractional change from the immediately previous row by
        default. This is useful in comparing the fraction of change in a time
        series of elements.

        .. note::

            Despite the name of this method, it calculates fractional change
            (also known as per unit change or relative change) and not
            percentage change. If you need the percentage change, multiply
            these values by 100.

        Parameters
        ----------
        periods : int, default 1
            Periods to shift for forming percent change.
        fill_method : {'backfill', 'bfill', 'pad', 'ffill', None}, default 'pad'
            How to handle NAs **before** computing percent changes.

            .. deprecated:: 2.1

        limit : int, default None
            The number of consecutive NAs to fill before stopping.

            .. deprecated:: 2.1

        freq : DateOffset, timedelta, or str, optional
            Increment to use from time series API (e.g. 'M' or BDay()).
        **kwargs
            Additional keyword arguments are passed into
            `DataFrame.shift` or `Series.shift`.

        Returns
        -------
        Series or DataFrame
            The same type as the calling object.

        See Also
        --------
        Series.diff : Compute the difference of two elements in a Series.
        DataFrame.diff : Compute the difference of two elements in a DataFrame.
        Series.shift : Shift the index by some number of periods.
        DataFrame.shift : Shift the index by some number of periods.

        Examples
        --------
        **Series**

        >>> s = pd.Series([90, 91, 85])
        >>> s
        0    90
        1    91
        2    85
        dtype: int64

        >>> s.pct_change()
        0         NaN
        1    0.011111
        2   -0.065934
        dtype: float64

        >>> s.pct_change(periods=2)
        0         NaN
        1         NaN
        2   -0.055556
        dtype: float64

        See the percentage change in a Series where filling NAs with last
        valid observation forward to next valid.

        >>> s = pd.Series([90, 91, None, 85])
        >>> s
        0    90.0
        1    91.0
        2     NaN
        3    85.0
        dtype: float64

        >>> s.ffill().pct_change()
        0         NaN
        1    0.011111
        2    0.000000
        3   -0.065934
        dtype: float64

        **DataFrame**

        Percentage change in French franc, Deutsche Mark, and Italian lira from
        1980-01-01 to 1980-03-01.

        >>> df = pd.DataFrame({
        ...     'FR': [4.0405, 4.0963, 4.3149],
        ...     'GR': [1.7246, 1.7482, 1.8519],
        ...     'IT': [804.74, 810.01, 860.13]},
        ...     index=['1980-01-01', '1980-02-01', '1980-03-01'])
        >>> df
                        FR      GR      IT
        1980-01-01  4.0405  1.7246  804.74
        1980-02-01  4.0963  1.7482  810.01
        1980-03-01  4.3149  1.8519  860.13

        >>> df.pct_change()
                          FR        GR        IT
        1980-01-01       NaN       NaN       NaN
        1980-02-01  0.013810  0.013684  0.006549
        1980-03-01  0.053365  0.059318  0.061876

        Percentage of change in GOOG and APPL stock volume. Shows computing
        the percentage change between columns.

        >>> df = pd.DataFrame({
        ...     '2016': [1769950, 30586265],
        ...     '2015': [1500923, 40912316],
        ...     '2014': [1371819, 41403351]},
        ...     index=['GOOG', 'APPL'])
        >>> df
                  2016      2015      2014
        GOOG   1769950   1500923   1371819
        APPL  30586265  40912316  41403351

        >>> df.pct_change(axis='columns', periods=-1)
                  2016      2015  2014
        GOOG  0.179241  0.094112   NaN
        APPL -0.252395 -0.011860   NaN
        """
        # GH#53491
        if fill_method is not lib.no_default or limit is not lib.no_default:
            warnings.warn(
                "The 'fill_method' and 'limit' keywords in "
                f"{type(self).__name__}.pct_change are deprecated and will be "
                "removed in a future version. Call "
                f"{'bfill' if fill_method in ('backfill', 'bfill') else 'ffill'} "
                "before calling pct_change instead.",
                FutureWarning,
                stacklevel=find_stack_level(),
            )
        if fill_method is lib.no_default:
            if self.isna().values.any():
                warnings.warn(
                    "The default fill_method='pad' in "
                    f"{type(self).__name__}.pct_change is deprecated and will be "
                    "removed in a future version. Call ffill before calling "
                    "pct_change to retain current behavior and silence this warning.",
                    FutureWarning,
                    stacklevel=find_stack_level(),
                )
            fill_method = "pad"
        if limit is lib.no_default:
            limit = None

        axis = self._get_axis_number(kwargs.pop("axis", "index"))
        if fill_method is None:
            data = self
        else:
            data = self._pad_or_backfill(fill_method, axis=axis, limit=limit)

        shifted = data.shift(periods=periods, freq=freq, axis=axis, **kwargs)
        # Unsupported left operand type for / ("Self")
        rs = data / shifted - 1  # type: ignore[operator]
        if freq is not None:
            # Shift method is implemented differently when freq is not None
            # We want to restore the original index
            rs = rs.loc[~rs.index.duplicated()]
            rs = rs.reindex_like(data)
        return rs.__finalize__(self, method="pct_change")
